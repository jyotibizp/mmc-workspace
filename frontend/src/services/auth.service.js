import apiClient from '../api/client';

export const authService = {
  // Get current user profile
  getProfile: async () => {
    const response = await apiClient.get('/auth/profile');
    return response.data;
  },

  // Update user profile
  updateProfile: async (profileData) => {
    const response = await apiClient.put('/auth/profile', profileData);
    return response.data;
  },

  // Get user permissions
  getPermissions: async () => {
    const response = await apiClient.get('/auth/permissions');
    return response.data;
  },

  // Verify token validity
  verifyToken: async () => {
    const response = await apiClient.get('/auth/verify');
    return response.data;
  }
};