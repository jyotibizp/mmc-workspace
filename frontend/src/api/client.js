import axios from 'axios';

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Store for Auth0 functions
let getAccessTokenSilently = null;
let logout = null;

// Initialize Auth0 functions
export const initializeAuth = (tokenGetter, logoutFn) => {
  getAccessTokenSilently = tokenGetter;
  logout = logoutFn;
};

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  async (config) => {
    try {
      if (getAccessTokenSilently) {
        const token = await getAccessTokenSilently({
          audience: "https://api.mapmyclient.com",
          scope: 'openid profile email'
        });
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('Error getting access token:', error);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const { response, request, message } = error;

    if (response) {
      // Server responded with error status
      switch (response.status) {
        case 401:
          console.error('Unauthorized access - token may be expired');
          if (logout) {
            logout({ returnTo: window.location.origin });
          }
          break;
        case 403:
          console.error('Forbidden access - insufficient permissions');
          break;
        case 404:
          console.error('Resource not found');
          break;
        case 422:
          console.error('Validation error:', response.data);
          break;
        case 500:
          console.error('Internal server error');
          break;
        default:
          console.error('API Error:', response.status, response.data);
      }
    } else if (request) {
      // Network error
      console.error('Network error - please check your connection');
    } else {
      // Something else happened
      console.error('Request error:', message);
    }

    return Promise.reject(error);
  }
);

export default apiClient;