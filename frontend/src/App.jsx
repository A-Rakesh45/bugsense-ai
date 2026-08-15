import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Sidebar } from './components/Sidebar';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { BugList } from './pages/BugList';
import { BugCreate } from './pages/BugCreate';
import { BugDetail } from './pages/BugDetail';
import { Analytics } from './pages/Analytics';
import { ModelPerformance } from './pages/ModelPerformance';
import { FeedbackLogs } from './pages/FeedbackLogs';

const ProtectedLayout = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div style={{ padding: '40px', textAlign: 'center' }}>Authenticating user session...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="app-container">
      <Sidebar />
      <div className="main-wrapper">
        <header className="top-header">
          <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-secondary)' }}>
            Environment: <span style={{ color: '#10b981' }}>Production</span> &bull; Engine: <span style={{ color: 'var(--accent-primary)' }}>Joblib TF-IDF v1.0</span>
          </div>
          <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
            Logged in as: <b>{user.username}</b> ({user.role})
          </div>
        </header>
        <main className="content-area">
          {children}
        </main>
      </div>
    </div>
  );
};

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          <Route path="/dashboard" element={<ProtectedLayout><Dashboard /></ProtectedLayout>} />
          <Route path="/bugs" element={<ProtectedLayout><BugList /></ProtectedLayout>} />
          <Route path="/bugs/new" element={<ProtectedLayout><BugCreate /></ProtectedLayout>} />
          <Route path="/bugs/:id" element={<ProtectedLayout><BugDetail /></ProtectedLayout>} />
          <Route path="/analytics" element={<ProtectedLayout><Analytics /></ProtectedLayout>} />
          <Route path="/models" element={<ProtectedLayout><ModelPerformance /></ProtectedLayout>} />
          <Route path="/feedback" element={<ProtectedLayout><FeedbackLogs /></ProtectedLayout>} />

          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
