import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { bugService } from '../services/bugService';
import { StatusBadge } from '../components/StatusBadge';
import { Search, Filter, Plus, ArrowRight } from 'lucide-react';

export const BugList = () => {
  const [bugs, setBugs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [severityFilter, setSeverityFilter] = useState('');

  const fetchBugs = () => {
    setLoading(true);
    bugService.getBugs({
      search: search || undefined,
      status: statusFilter || undefined,
      severity: severityFilter || undefined
    })
      .then((data) => setBugs(data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchBugs();
  }, [statusFilter, severityFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchBugs();
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h1 className="page-title">Bug Tracker & Quality Queue</h1>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '2px' }}>
            Manage, search, and monitor AI-analyzed software defect reports
          </p>
        </div>
        <Link to="/bugs/new" className="btn btn-primary">
          <Plus size={16} /> Submit New Bug
        </Link>
      </div>

      {/* Filter Bar */}
      <div className="card" style={{ marginBottom: '20px', padding: '16px 20px' }}>
        <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', alignItems: 'center' }}>
          <div style={{ flex: 1, minWidth: '240px', position: 'relative' }}>
            <Search size={16} style={{ position: 'absolute', left: '12px', top: '11px', color: 'var(--text-muted)' }} />
            <input 
              type="text" 
              className="input-field" 
              placeholder="Search title, description, or module..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{ paddingLeft: '36px' }}
            />
          </div>

          <div style={{ minWidth: '150px' }}>
            <select 
              className="select-field" 
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="">All Statuses</option>
              <option value="Open">Open</option>
              <option value="In Progress">In Progress</option>
              <option value="Resolved">Resolved</option>
              <option value="Closed">Closed</option>
            </select>
          </div>

          <div style={{ minWidth: '150px' }}>
            <select 
              className="select-field" 
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
            >
              <option value="">All Severities</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>

          <button type="submit" className="btn btn-secondary">
            <Filter size={15} /> Search
          </button>
        </form>
      </div>

      {/* Table */}
      <div className="table-container">
        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
            Loading bug reports...
          </div>
        ) : bugs.length === 0 ? (
          <div style={{ padding: '48px', textAlign: 'center' }}>
            <h3 style={{ fontSize: '16px', color: 'var(--text-secondary)' }}>No matching bugs found</h3>
            <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '4px' }}>
              Try clearing search parameters or submit a new bug report.
            </p>
          </div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th style={{ width: '80px' }}>Bug ID</th>
                <th>Title</th>
                <th>Severity</th>
                <th>Priority</th>
                <th>Module</th>
                <th>Status</th>
                <th>AI Conf.</th>
                <th>Created</th>
                <th style={{ width: '80px' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {bugs.map((bug) => (
                <tr key={bug.id}>
                  <td style={{ fontWeight: 700, color: 'var(--text-muted)' }}>
                    #{String(bug.id).padStart(4, '0')}
                  </td>
                  <td style={{ fontWeight: 600 }}>
                    <Link to={`/bugs/${bug.id}`} style={{ color: 'var(--text-primary)' }}>
                      {bug.title}
                    </Link>
                  </td>
                  <td>
                    <StatusBadge type="severity" value={bug.prediction?.predicted_severity || 'Medium'} />
                  </td>
                  <td>
                    <StatusBadge type="priority" value={bug.prediction?.predicted_priority || 'P3'} />
                  </td>
                  <td>
                    <span style={{ fontSize: '12px', background: 'var(--bg-subtle)', padding: '3px 8px', borderRadius: '4px', border: '1px solid var(--border-color)' }}>
                      {bug.module}
                    </span>
                  </td>
                  <td>
                    <StatusBadge type="status" value={bug.status} />
                  </td>
                  <td style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>
                    {bug.prediction ? `${Math.round(bug.prediction.confidence * 100)}%` : 'N/A'}
                  </td>
                  <td style={{ color: 'var(--text-muted)', fontSize: '12.5px' }}>
                    {new Date(bug.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  </td>
                  <td>
                    <Link to={`/bugs/${bug.id}`} className="btn btn-secondary" style={{ padding: '4px 8px', fontSize: '12px' }}>
                      Inspect <ArrowRight size={13} />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};
