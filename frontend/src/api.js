// api.js - API configuration
// Using environment variable for API base URL to support both dev and prod environments
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Validate the API_BASE_URL format
let validatedApiBaseUrl = API_BASE_URL;
try {
  new URL(API_BASE_URL); // This will throw an error if the URL is invalid
} catch (error) {
  console.error(`Invalid API_BASE_URL: "${API_BASE_URL}". Using default value.`, error);
  validatedApiBaseUrl = 'http://localhost:8000'; // Fallback to default
}

export default validatedApiBaseUrl;

// Helper function to get user ID from auth context
// This would typically be called from components that have access to the auth context
export const getUserIdFromToken = (token) => {
  if (!token) return null;

  try {
    // Decode JWT token to extract user ID
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    const decodedToken = JSON.parse(jsonPayload);
    return decodedToken.user_id || decodedToken.sub; // sub is commonly used for user ID in JWTs
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};