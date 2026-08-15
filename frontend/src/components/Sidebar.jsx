import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Bug, 
  PlusCircle, 
  BarChart3, 
  Cpu, 
  MessageSquare,
  LogOut,
  ShieldCheck
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const Sidebar = () => {
  const { user, logout } = useAuth();

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo-mark">
          <ShieldCheck size={20} />
        </div>
        <div>
          <div className="logo-text">BugSense AI</div>
          <div className="logo-tagline">Intelligent Software Quality</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-label">Core Management</div>
        <NavLink to="/dashboard" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <LayoutDashboard size={17} /> Overview
        </NavLink>
        <NavLink to="/bugs" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <Bug size={17} /> Bug Tracker
        </NavLink>
        <NavLink to="/bugs/new" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <PlusCircle size={17} /> Submit Bug Report
        </NavLink>

        <div className="nav-section-label">AI & Intelligence</div>
        <NavLink to="/analytics" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <BarChart3 size={17} /> Analytics & Risk
        </NavLink>
        <NavLink to="/models" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <Cpu size={17} /> Model Monitoring
        </NavLink>
        <NavLink to="/feedback" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <MessageSquare size={17} /> Prediction Feedback
        </NavLink>
      </nav>

      {user && (
        <div className="sidebar-footer">
          <div className="user-profile">
            <div className="avatar">{user.username.charAt(0).toUpperCase()}</div>
            <div>
              <div style={{ fontWeight: 600, fontSize: '13px', color: 'var(--text-primary)' }}>
                {user.username}
              </div>
              <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                Role: {user.role}
              </div>
            </div>
          </div>
          <button 
            onClick={logout} 
            title="Log Out"
            style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)', padding: '4px' }}
          >
            <LogOut size={16} />
          </button>
        </div>
      )}
    </aside>
  );
};
