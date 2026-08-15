import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { bugService } from '../services/bugService';
import { Cpu, AlertCircle, CheckCircle2 } from 'lucide-react';

export const BugCreate = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    steps_to_reproduce: '',
    expected_result: '',
    actual_result: '',
    environment: 'Production',
    app_version: 'v1.0.0',
    browser_device: 'Chrome 120 / Windows 11',
    module: 'General'
  });

  const [loading, setLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    setLoadingStage('Cleaning & tokenizing text signals...');

    try {
      setTimeout(() => setLoadingStage('Transforming features with TF-IDF vectorizer...'), 300);
      setTimeout(() => setLoadingStage('Executing ML multi-class classifiers & Risk Engine...'), 600);
      setTimeout(() => setLoadingStage('Calculating cosine similarity against historical bugs...'), 900);

      const createdBug = await bugService.createBug(formData);
      setTimeout(() => {
        navigate(`/bugs/${createdBug.id}`);
      }, 1200);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit bug report.');
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 className="page-title">Submit Bug Report</h1>
        <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '2px' }}>
          Provide defect reproduction details. BugSense AI will instantly predict severity, priority, category, risk score, and find similar bugs.
        </p>
      </div>

      {error && (
        <div style={{
          backgroundColor: '#fef2f2',
          border: '1px solid #fecaca',
          color: '#991b1b',
          padding: '12px',
          borderRadius: '6px',
          fontSize: '13px',
          marginBottom: '20px',
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          <AlertCircle size={16} /> {error}
        </div>
      )}

      {loading ? (
        <div className="card" style={{ padding: '48px', textAlign: 'center' }}>
          <div style={{
            width: '48px',
            height: '48px',
            backgroundColor: 'var(--status-open-bg)',
            color: 'var(--accent-primary)',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 16px auto'
          }}>
            <Cpu size={24} className="animate-spin" />
          </div>
          <h3 style={{ fontSize: '17px', marginBottom: '8px' }}>Analyzing Bug Report with AI</h3>
          <p style={{ fontSize: '13.5px', color: 'var(--text-secondary)', fontWeight: 500 }}>
            {loadingStage}
          </p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="card" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '12px', fontWeight: 700, fontSize: '15px' }}>
            1. Bug Summary & Description
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, marginBottom: '6px' }}>
              Bug Title <span style={{ color: '#ef4444' }}>*</span>
            </label>
            <input 
              type="text" 
              className="input-field"
              placeholder="e.g. SQL Injection vulnerability in authentication token parser"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              required 
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, marginBottom: '6px' }}>
              Detailed Description <span style={{ color: '#ef4444' }}>*</span>
            </label>
            <textarea 
              className="textarea-field"
              rows={4}
              placeholder="Provide complete details regarding the defect behavior, error messages, and subsystem impact..."
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              required 
            />
          </div>

          <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '12px', fontWeight: 700, fontSize: '15px', marginTop: '8px' }}>
            2. Reproduction & Behavior Details
          </div>

          <div className="grid-2">
            <div>
              <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, marginBottom: '6px' }}>
                Steps to Reproduce
              </label>
              <textarea 
                className="textarea-field"
                rows={3}
                placeholder="1. Navigate to...\n2. Click on...\n3. Observe error..."
                value={formData.steps_to_reproduce}
                onChange={(e) => setFormData({ ...formData, steps_to_reproduce: e.target.value })}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, marginBottom: '6px' }}>
                Expected vs Actual Result
              </label>
              <textarea 
                className="textarea-field"
                rows={3}
                placeholder="Expected: Input validated cleanly\nActual: 500 error thrown..."
                value={formData.actual_result}
                onChange={(e) => setFormData({ ...formData, actual_result: e.target.value })}
              />
            </div>
          </div>

          <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '12px', fontWeight: 700, fontSize: '15px', marginTop: '8px' }}>
            3. Environment & Classification
          </div>

          <div className="grid-2">
            <div>
              <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, marginBottom: '6px' }}>
                Subsystem Module
              </label>
              <select 
                className="select-field"
                value={formData.module}
                onChange={(e) => setFormData({ ...formData, module: e.target.value })}
              >
                <option value="General">General</option>
                <option value="Authentication">Authentication</option>
                <option value="Payment">Payment</option>
                <option value="Database">Database</option>
                <option value="Network">Network</option>
                <option value="UI/UX">UI/UX</option>
                <option value="Performance">Performance</option>
                <option value="Integration">Integration</option>
                <option value="Security">Security</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, marginBottom: '6px' }}>
                Deployment Environment
              </label>
              <select 
                className="select-field"
                value={formData.environment}
                onChange={(e) => setFormData({ ...formData, environment: e.target.value })}
              >
                <option value="Production">Production</option>
                <option value="Staging">Staging</option>
                <option value="Development">Development</option>
              </select>
            </div>
          </div>

          <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
            <button type="button" onClick={() => navigate('/bugs')} className="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" style={{ padding: '10px 24px', fontSize: '14px' }}>
              <Cpu size={16} /> Analyze with BugSense AI
            </button>
          </div>
        </form>
      )}
    </div>
  );
};
