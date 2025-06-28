import api from './api';
import { UserCreate, UserLogin } from '../types/index';

export const authApi = {
  login: async (userData: UserLogin) => {
    const formData = new URLSearchParams();
    formData.append('username', userData.email); // The backend expects 'username' for the email
    formData.append('password', userData.password);

    const response = await api.post('/token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return response.data;
  },

  register: async (userData: UserCreate) => {
    const response = await api.post('/users/', userData);
    return response.data;
  },
};
