import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useAuth0, withAuthenticationRequired } from '@auth0/auth0-react';
import { initializeAuth } from './api/client';
import LoginButton from './components/LoginButton';
import ProtectedRoute from './components/ProtectedRoute';
import MainLayout from './components/Layout/MainLayout';
import Dashboard from './pages/Dashboard';
import LinkedInPosts from './pages/LinkedInPosts';
import Opportunities from './pages/Opportunities';
import Proposals from './pages/Proposals';
import Campaigns from './pages/Campaigns';
import Companies from './pages/Companies';
import Contacts from './pages/Contacts';
import Settings from './pages/Settings';
import './App.css'

function App() {
  const { isAuthenticated, isLoading, getAccessTokenSilently, logout } = useAuth0();

  // Initialize API client with Auth0 functions
  useEffect(() => {
    if (isAuthenticated) {
      initializeAuth(getAccessTokenSilently, logout);
    }
  }, [isAuthenticated, getAccessTokenSilently, logout]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            {import.meta.env.VITE_APP_TITLE || 'MapMyClient'}
          </h1>
          <p className="text-lg text-gray-600 mb-8">
            Please log in to access your dashboard and manage opportunities.
          </p>
          <LoginButton />
        </div>
      </div>
    );
  }

  return (
    <Router>
      <ProtectedRoute>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<Dashboard />} />
            <Route path="posts" element={<LinkedInPosts />} />
            <Route path="opportunities" element={<Opportunities />} />
            <Route path="proposals" element={<Proposals />} />
            <Route path="campaigns" element={<Campaigns />} />
            <Route path="companies" element={<Companies />} />
            <Route path="contacts" element={<Contacts />} />
            <Route path="settings" element={<Settings />} />
          </Route>
        </Routes>
      </ProtectedRoute>
    </Router>
  );
}

export default App
