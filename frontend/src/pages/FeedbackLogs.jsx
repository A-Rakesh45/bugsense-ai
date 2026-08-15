import React, { useState, useEffect } from 'react';
import { dashboardService } from '../services/dashboardService';
import { StatusBadge } from '../components/StatusBadge';
import { MessageSquare, Plus, CheckCircle } from 'lucide-react';

export const FeedbackLogs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({
    prediction_id: 1,
    corrected_severity: 'High',
    corrected_priority: 'P2',
    corrected_category: 'Functional',
    notes: ''
  });

  const fetchLogs = () => {
    setLoading(true);
    dashboardService.getFeedbackLogs()
      .then((data) => setLogs(data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  const handleSubmitCorrection = async (e) => {
    e.preventDefault();
    try {
      await dashboardService.submitFeedback(form);
      setShowModal(false);
      fetchLogs();
    } catch (err) {
      alert('Failed to submit correction');
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h1 className="page-title">AI Prediction Feedback Audit</h1>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '2px' }}>
            Human-in-the-loop review log for model retraining & quality auditing
          </p>
        </div>
        <button onClick={() => setShowModal(true)} className="btn btn-primary">
          <Plus size={16} /> Submit AI Correction
        </button>
      </div>

      <div className="table-container">
        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>Loading feedback logs...</div>
        ) : logs.length === 0 ? (
          <div style={{ padding: '48px', textAlign: 'center' }}>
            <h3 style={{ fontSize: '16px', color: 'var(--text-secondary)' }}>No prediction corrections logged yet</h3>
            <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '4px' }}>
              When QA testers or Admins correct an AI prediction, audit logs appear here.
            </p>
          </div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Audit ID</th>
                <th>Prediction ID</th>
                <th>Corrected Severity</th>
                <th>Corrected Priority</th>
                <th>Reviewed By</th>
                <th>Model Ver.</th>
                <th>Notes</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log) => (
                <tr key={log.id}>
                  <td style={{ fontWeight: 700 }}>#{String(log.id).padStart(4, '0')}</td>
                  <td>Pred #{log.prediction_id}</td>
                  <td><StatusBadge type="severity" value={log.corrected_severity || 'High'} /></td>
                  <td><StatusBadge type="priority" value={log.corrected_priority || 'P2'} /></td>
                  <td>{log.corrected_by?.username} ({log.corrected_by?.role})</td>
                  <td><span style={{ fontSize: '12px', background: 'var(--bg-subtle)', padding: '2px 6px', borderRadius: '4px' }}>{log.model_version}</span></td>
                  <td style={{ color: 'var(--text-secondary)', fontSize: '12.5px' }}>{log.notes || 'N/A'}</td>
                  <td style={{ color: 'var(--text-muted)', fontSize: '12px' }}>{new Date(log.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Modal for adding correction */}
      {showModal && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          backgroundColor: 'rgba(15, 23, 42, 0.4)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000
        }}>
          <div className="card" style={{ width: '420px', padding: '24px' }}>
            <h3 style={{ fontSize: '17px', marginBottom: '16px' }}>Submit AI Correction</h3>
            <form onSubmit={handleSubmitCorrection} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, marginBottom: '4px' }}>
                  Prediction ID
                </label>
                <input 
                  type="number" 
                  className="input-field" 
                  value={form.prediction_id}
                  onChange={(e) => setForm({ ...form, prediction_id: parseInt(e.target.value) })}
                  required 
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, marginBottom: '4px' }}>
                  Corrected Severity
                </label>
                <select 
                  className="select-field"
                  value={form.corrected_severity}
                  onChange={(e) => setForm({ ...form, corrected_severity: e.target.value })}
                >
                  <option value="Critical">Critical</option>
                  <option value="High">High</option>
                  <option value="Medium">Medium</option>
                  <option value="Low">Low</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, marginBottom: '4px' }}>
                  Corrected Priority
                </label>
                <select 
                  className="select-field"
                  value={form.corrected_priority}
                  onChange={(e) => setForm({ ...form, corrected_priority: e.target.value })}
                >
                  <option value="P1">P1</option>
                  <option value="P2">P2</option>
                  <option value="P3">P3</option>
                  <option value="P4">P4</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, marginBottom: '4px' }}>
                  Reviewer Notes
                </label>
                <textarea 
                  className="textarea-field" 
                  rows={3} 
                  placeholder="Reason for correction..."
                  value={form.notes}
                  onChange={(e) => setForm({ ...form, notes: e.target.value })}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', marginTop: '12px' }}>
                <button type="button" onClick={() => setShowModal(false)} className="btn btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Save Correction
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
