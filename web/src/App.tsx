import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

// Pages
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import AnalysisPage from './pages/AnalysisPage';
import PuzzlesPage from './pages/PuzzlesPage';
import AiCoachPage from './pages/AiCoachPage';

import ReviewPage from './pages/Review';
import LessonsPage from './pages/Lessons';
import PlayCoachPage from './pages/PlayCoach';
import NotFound from './pages/NotFound';
import AuthGatewayPage from './pages/AuthGatewayPage';

// Components
import Layout from './components/Layout';
import { AuthProvider } from './context/AuthContext';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/auth" element={<AuthGatewayPage />} />
        <Route path="/app" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="dashboard" element={<Navigate to="/app" replace />} />
          <Route path="analysis" element={<AnalysisPage />} />
          <Route path="puzzles" element={<PuzzlesPage />} />
          <Route path="ai-coach" element={<AiCoachPage />} />
          <Route path="review" element={<ReviewPage />} />
          <Route path="lessons" element={<LessonsPage />} />
          <Route path="play" element={<PlayCoachPage />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </AuthProvider>
  );
};

export default App;
