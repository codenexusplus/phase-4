import React, { createContext, useContext, useState } from 'react';
import axios from 'axios';
import API_BASE_URL from '../api';

// Create Auth Context
const AuthContext = createContext();

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Auth Provider Component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [loading, setLoading] = useState(false);

  // Set up axios interceptor to include token in requests
  React.useEffect(() => {
    const requestInterceptor = axios.interceptors.request.use(
      (config) => {
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    return () => {
      axios.interceptors.request.eject(requestInterceptor);
    };
  }, [token]);

  // Register function
  const register = async (userData) => {
    setLoading(true);
    try {
      // Validate API_BASE_URL before making the request
      if (!API_BASE_URL) {
        throw new Error('API_BASE_URL is not defined. Please check your environment variables.');
      }

      const response = await axios.post(`${API_BASE_URL}/api/auth/register`, userData);
      localStorage.setItem('token', response.data.access_token);
      setToken(response.data.access_token);
      setUser(response.data.user);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Registration error:', error);
      return { success: false, error: error.response?.data?.detail || error.message || 'Registration failed' };
    } finally {
      setLoading(false);
    }
  };

  // Login function
  const login = async (credentials) => {
    setLoading(true);
    try {
      // Validate API_BASE_URL before making the request
      if (!API_BASE_URL) {
        throw new Error('API_BASE_URL is not defined. Please check your environment variables.');
      }

      const response = await axios.post(`${API_BASE_URL}/api/auth/login`, credentials);
      localStorage.setItem('token', response.data.access_token);
      setToken(response.data.access_token);
      setUser(response.data.user);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: error.response?.data?.detail || error.message || 'Login failed' };
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  // Get user profile
  const getUserProfile = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/auth/me`);
      setUser(response.data);
      return response.data;
    } catch (error) {
      console.error('Error getting user profile:', error);
      // Only log out if it's an auth error (401), not for network errors
      if (error.response && error.response.status === 401) {
        logout(); // If token is invalid, log out the user
      }
      return null;
    }
  };

  const value = {
    user,
    token,
    loading,
    register,
    login,
    logout,
    getUserProfile
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};