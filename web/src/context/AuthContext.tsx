import React, { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api'; // Use the configured axios instance

// Helper to convert FastAPI/Pydantic validation errors into a user-friendly string
const getErrorMessage = (err: any): string => {
  const detail = err?.response?.data?.detail;
  if (Array.isArray(detail)) {
    // FastAPI validation errors come back as an array of error objects
    return detail.map((d: any) => d.msg || 'Validation error').join('\n');
  }
  if (typeof detail === 'string') {
    return detail;
  }
  if (err?.message) {
    return err.message;
  }
  return 'Unexpected error, please try again.';
};

interface User {
  id: number;
  email: string;
  username: string;
  elo_rating: number;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, username: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true); // Start with loading true
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const logout = useCallback(() => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    delete api.defaults.headers.common['Authorization'];
    navigate('/login');
  }, [navigate]);

  const fetchUserData = useCallback(async (authToken: string) => {
    api.defaults.headers.common['Authorization'] = `Bearer ${authToken}`;
    try {
      const response = await api.get('/api/users/me');
      setUser(response.data);
    } catch (err) {
      console.error('Failed to fetch user data, logging out.', err);
      logout();
    } finally {
      setLoading(false);
    }
  }, [logout]);

  useEffect(() => {
    if (token) {
      fetchUserData(token);
    } else {
      setLoading(false); // Not logged in, stop loading
    }
  }, [token, fetchUserData]);

  const login = async (email: string, password: string) => {
    setLoading(true);
    setError(null);
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const response = await api.post('/api/auth/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      setToken(access_token);
      await fetchUserData(access_token);
      navigate('/');
    } catch (err: any) {
      setError(getErrorMessage(err));
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const register = async (email: string, password: string, username: string) => {
    setLoading(true);
    setError(null);
    try {
      await api.post('/api/auth/users/', { email, password, username });
      // After successful registration, log the user in
      await login(email, password);
    } catch (err: any) {
      setError(getErrorMessage(err));
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const value = {
    user,
    token,
    login,
    register,
    logout,
    isAuthenticated: !!token,
    loading,
    error,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
