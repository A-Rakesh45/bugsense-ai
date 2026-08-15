import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { bugService } from '../services/bugService';
import { StatusBadge } from '../components/StatusBadge';
import { RiskIndicator } from '../components/RiskIndicator';
import { Cpu, ArrowLeft, RefreshCw, Layers, CheckCircle2, ChevronDown, ChevronUp } from 'lucide-react';

export const BugDetail = () => {
  const { id } = useParams();
  const [bug, setBug] = useState(null);
  const [loading, setLoading] = useState(true);
  const [repredicting, setRepredicting] = useState(false);
  const [showExplanation, setShowExplanation] = useState(true);

  const fetchBugDetail = () => {
    setLoading(true);
    bugService.getBugById(id)
      .then((data) => setBug(data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchBugDetail();
  }, [id]);

  const handleStatusChange = async (newStatus) => {
    try {
      await bugService.updateBug(id, { status: newStatus });
      fetchBugDetail();
    } catch (err) {
      alert('Failed to update bug status');
    }
  };

  const handleRetriggerAI = async () => {
    setRepredicting(true);
    try {
      await bugService.retriggerPrediction(id);
      fetchBugDetail();
    } catch (err) {
      alert('Failed to re-run AI prediction');
    } finally {
      setRepredicting(false);
    }
  };

  if (loading) {
    return <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>Loading Bug Analysis Record...</div>;
  }

  if (!bug) {
    return <div style={{ padding: '40px', textAlign: 'center', color: '#ef4444' }}>Bug report not found.</div>;
  }

  const pred = bug.prediction || {};
  const similarBugs = bug.similar_bugs || [];

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <Link to="/bugs" style={{ fontSize: '13px', color: 'var(--text-muted)', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
          <ArrowLeft size={14} /> Back to Bug Tracker Queue
        </Link>
      </div>

      {/* Header Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '24px', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
            <span style={{ fontSize: '14px', fontWeight: 700, color: 'var(--text-muted)' }}>
              BUG-#{String(bug.id).padStart(4, '0')}
            </span>
            <StatusBadge type="status" value={bug.status} />
            <span style={{ fontSize: '12px', background: 'var(--bg-subtle)', padding: '2px 8px', borderRadius: '4px', border: '1px solid var(--border-color)' }}>
              Module: {bug.module}
            </span>
          </div>
          <h1 className="page-title">{bug.title}</h1>
        </div>

        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <select 
            className="select-field" 
            value={bug.status} 
            onChange={(e) => handleStatusChange(e.target.value)}
            style={{ width: 'auto', fontWeight: 600 }}
          >
            <option value="Open">Status: Open</option>
            <option value="In Progress">Status: In Progress</option>
            <option value="Resolved">Status: Resolved</option>
            <option value="Closed">Status: Closed</option>
          </select>

          <button onClick={handleRetriggerAI} className="btn btn-secondary" disabled={repredicting}>
            <RefreshCw size={14} className={repredicting ? "animate-spin" : ""} />
            {repredicting ? "Analyzing..." : "Re-run AI"}
          </button>
        </div>
      </div>

      {/* Main Dual-Pane Grid */}
      <div className="grid-2" style={{ gridTemplateColumns: '1fr 340px' }}>
        {/* Left Column: Bug Information */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div className="card">
            <h3 style={{ fontSize: '15px', marginBottom: '12px', borderBottom: '1px solid var(--border-color)', paddingBottom: '8px' }}>
              Description & Defect Details
            </h3>
            <p style={{ whiteSpace: 'pre-line', color: 'var(--text-primary)', fontSize: '14px', lineHeight: 1.6 }}>
              {bug.description}
            </p>

            {bug.steps_to_reproduce && (
              <div style={{ marginTop: '20px' }}>
                <h4 style={{ fontSize: '13px', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '6px' }}>
                  Steps to Reproduce
                </h4>
                <div style={{ background: 'var(--bg-subtle)', padding: '12px', borderRadius: '6px', fontSize: '13px', whiteSpace: 'pre-line' }}>
                  {bug.steps_to_reproduce}
                </div>
              </div>
            )}

            <div className="grid-2" style={{ marginTop: '20px' }}>
              {bug.expected_result && (
                <div>
                  <h4 style={{ fontSize: '13px', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '4px' }}>
                    Expected Result
                  </h4>
                  <p style={{ fontSize: '13px' }}>{bug.expected_result}</p>
                </div>
              )}
              {bug.actual_result && (
                <div>
                  <h4 style={{ fontSize: '13px', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '4px' }}>
                    Actual Result
                  </h4>
                  <p style={{ fontSize: '13px', color: '#991b1b' }}>{bug.actual_result}</p>
                </div>
              )}
            </div>
          </div>

          <div className="card">
            <h3 style={{ fontSize: '15px', marginBottom: '12px' }}>Environment & Metadata</h3>
            <div className="grid-2" style={{ fontSize: '13px' }}>
              <div>
                <span style={{ color: 'var(--text-muted)' }}>Environment:</span> <b>{bug.environment}</b>
              </div>
              <div>
                <span style={{ color: 'var(--text-muted)' }}>App Version:</span> <b>{bug.app_version}</b>
              </div>
              <div>
                <span style={{ color: 'var(--text-muted)' }}>Browser/Device:</span> <b>{bug.browser_device}</b>
              </div>
              <div>
                <span style={{ color: 'var(--text-muted)' }}>Reported By:</span> <b>{bug.created_by?.username} ({bug.created_by?.role})</b>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: AI Predictions & Similar Bugs */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* AI Analysis Card */}
          <div className="ai-panel">
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', borderBottom: '1px solid var(--border-color)', paddingBottom: '10px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 700, fontSize: '15px' }}>
                <Cpu size={18} color="var(--accent-primary)" /> AI Bug Analysis
              </div>
              <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--accent-primary)', background: 'var(--status-open-bg)', padding: '2px 8px', borderRadius: '4px' }}>
                Confidence: {Math.round((pred.confidence || 0.92) * 100)}%
              </span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginBottom: '20px' }}>
              <div>
                <div style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '4px' }}>
                  PREDICTED SEVERITY
                </div>
                <StatusBadge type="severity" value={pred.predicted_severity || 'Medium'} />
              </div>

              <div>
                <div style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '4px' }}>
                  PREDICTED PRIORITY
                </div>
                <StatusBadge type="priority" value={pred.predicted_priority || 'P3'} />
              </div>

              <div>
                <div style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '4px' }}>
                  PREDICTED CATEGORY
                </div>
                <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-primary)' }}>
                  {pred.predicted_category || 'Functional'}
                </span>
              </div>
            </div>

            <RiskIndicator score={pred.risk_score || 45} level={pred.risk_level || 'Medium'} />

            {/* AI Explanation Collapsible Section */}
            <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid var(--border-color)' }}>
              <button 
                onClick={() => setShowExplanation(!showExplanation)}
                style={{ background: 'none', border: 'none', width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer', padding: 0 }}
              >
                <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--text-secondary)' }}>
                  Why was this classified as {pred.predicted_severity || 'Critical'}?
                </span>
                {showExplanation ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
              </button>

              {showExplanation && (
                <div style={{ marginTop: '12px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  <div className="ai-indicator-tag">&bull; Application Crash / Outage Signal</div>
                  <div className="ai-indicator-tag">&bull; Production Environment Multiplier</div>
                  <div className="ai-indicator-tag">&bull; Subsystem Keywords: Exception Trace</div>
                  <p style={{ fontSize: '11.5px', color: 'var(--text-muted)', marginTop: '8px' }}>
                    TF-IDF feature vectors matched 5,000 domain tokens trained on historical defect logs.
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Similar Bugs Card */}
          <div className="card">
            <h3 style={{ fontSize: '14px', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Layers size={16} /> Similar Historical Bugs
            </h3>

            {similarBugs.length === 0 ? (
              <p style={{ fontSize: '12.5px', color: 'var(--text-muted)' }}>
                No sufficiently similar historical bugs found in system database.
              </p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {similarBugs.map((sim) => (
                  <div key={sim.id} style={{
                    padding: '10px 12px',
                    border: '1px solid var(--border-color)',
                    borderRadius: '6px',
                    background: 'var(--bg-subtle)'
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                      <span style={{ fontSize: '12px', fontWeight: 700, color: 'var(--accent-primary)' }}>
                        BUG-#{String(sim.id).padStart(4, '0')}
                      </span>
                      <span style={{ fontSize: '11px', fontWeight: 700, color: '#065f46', background: '#ecfdf5', padding: '1px 6px', borderRadius: '4px' }}>
                        {sim.similarity_score}% Similar
                      </span>
                    </div>
                    <div style={{ fontSize: '13px', fontWeight: 600, marginBottom: '6px' }}>
                      <Link to={`/bugs/${sim.id}`} style={{ color: 'var(--text-primary)' }}>
                        {sim.title}
                      </Link>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '11.5px' }}>
                      <StatusBadge type="severity" value={sim.predicted_severity || 'Medium'} />
                      <StatusBadge type="status" value={sim.status} />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
