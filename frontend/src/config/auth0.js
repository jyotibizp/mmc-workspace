export const auth0Config = {
  domain: import.meta.env.VITE_AUTH0_DOMAIN,
  clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
  authorizationParams: {
    redirect_uri: window.location.origin,
    audience: "https://api.mapmyclient.com",
    scope: "openid profile email"
  },
  // Store tokens in localStorage to persist across page reloads
  cacheLocation: 'localstorage',
  // Use refresh tokens for seamless token renewal
  useRefreshTokens: true
};