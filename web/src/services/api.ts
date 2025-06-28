import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    // Handle 401 Unauthorized
    if (error.response?.status === 401) {
      // Clear auth data and redirect to the landing page
      localStorage.removeItem('token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/api/auth/login', { email, password }),
  register: (email: string, password: string, fullName: string) =>
    api.post('/api/auth/register', { email, password, full_name: fullName }),
  getMe: () => api.get('/api/users/me'),
};

// Analysis API
export const analysisAPI = {
  analyzePosition: (fen: string, depth: number = 18) =>
    api.post('/api/analyze/position', { fen, depth }),
  analyzeGame: (pgn: string) =>
    api.post('/api/analyze/game', { pgn }),
};

// Coach API
export const coachAPI = {
  askQuestion: (question: string, fen?: string, pgn?: string) =>
    api.post('/api/coach/ask', { question, fen, pgn }),
  getTrainingPlan: (timePerDay: number, daysPerWeek: number, focusAreas: string[]) =>
    api.post('/api/coach/training-plan', { time_per_day: timePerDay, days_per_week: daysPerWeek, focus_areas: focusAreas }),
};

// Puzzles API
export const puzzlesAPI = {
  getPuzzle: (difficulty?: string) =>
    api.get('/api/puzzles/next', { params: { difficulty } }),
  submitPuzzle: (puzzleId: number, isCorrect: boolean, timeSpent: number) =>
    api.post(`/api/puzzles/${puzzleId}/submit`, { is_correct: isCorrect, time_spent: timeSpent }),
};

// Games API
export const gamesAPI = {
  getGames: (limit: number = 10, offset: number = 0) =>
    api.get('/api/games', { params: { limit, offset } }),
  getGame: (id: number) =>
    api.get(`/api/games/${id}`),
  uploadGame: (pgn: string) =>
    api.post('/api/games/upload', { pgn }),
};

// Dashboard API
export const dashboardAPI = {
  getNewDashboardData: () => api.get('/api/dashboard/'),
};

export default api;
