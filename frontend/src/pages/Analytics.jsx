import React, { useState, useEffect } from 'react';
import { dashboardService } from '../services/dashboardService';
import { 
  Chart as ChartJS, 
  ArcElement, 
  Tooltip, 
  Legend, 
  CategoryScale, 
  LinearScale, 
  BarElement, 
  Title 
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';
import { BarChart3, ShieldCheck, Activity } from 'lucide-react';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

export const Analytics = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    dashboardService.getStatistics()
      .then((data) => setStats(data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>Loading Data Intelligence Analytics...</div>;
  }

  const charts = stats?.charts || {};

  const priorityChartData = {
    labels: ['P1 (Immediate)', 'P2 (High)', 'P3 (Normal)', 'P4 (Low)'],
    datasets: [
      {
        label: 'Bugs by Priority',
        data: [
          charts.priority_distribution?.P1 || 0,
          charts.priority_distribution?.P2 || 0,
          charts.priority_distribution?.P3 || 0,
          charts.priority_distribution?.P4 || 0,
        ],
        backgroundColor: ['#ef4444', '#f59e0b', '#2563eb', '#10b981'],
        borderRadius: 4,
      },
    ],
  };

  const categoryChartData = {
    labels: Object.keys(charts.category_distribution || {}),
    datasets: [
      {
        data: Object.values(charts.category_distribution || {}),
        backgroundColor: [
          '#2563eb', '#10b981', '#f59e0b', '#ef4444', 
          '#8b5cf6', '#ec4899', '#06b6d4', '#64748b'
        ],
        borderWidth: 0,
      },
    ],
  };

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 className="page-title">Software Intelligence & Analytics</h1>
        <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '2px' }}>
          Deep analytical metrics on bug classification, risk exposure, and defect patterns
        </p>
      </div>

      <div className="grid-2" style={{ marginBottom: '24px' }}>
        <div className="card">
          <h3 style={{ fontSize: '15px', marginBottom: '16px', color: 'var(--text-secondary)' }}>
            Priority Queue Distribution (P1 - P4)
          </h3>
          <div style={{ maxHeight: '260px' }}>
            <Bar data={priorityChartData} options={{ maintainAspectRatio: false, plugins: { legend: { display: false } } }} />
          </div>
        </div>

        <div className="card">
          <h3 style={{ fontSize: '15px', marginBottom: '16px', color: 'var(--text-secondary)' }}>
            Defect Categories (NLP Classified)
          </h3>
          <div style={{ maxHeight: '260px', display: 'flex', justifyContent: 'center' }}>
            <Pie data={categoryChartData} options={{ maintainAspectRatio: false, plugins: { legend: { position: 'right' } } }} />
          </div>
        </div>
      </div>

      {/* Risk Assessment Summary */}
      <div className="card">
        <h3 style={{ fontSize: '15px', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Activity size={18} /> Systemic Risk & Reliability Index
        </h3>
        <p style={{ fontSize: '13.5px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
          BugSense AI evaluates defect impact by weighting Severity (40%), Priority (35%), keyword threat indicators (+15%), and environment bonuses (+10%). Modules like <b>Security</b> and <b>Payment</b> trigger immediate high-priority triaging flags for engineering teams.
        </p>
      </div>
    </div>
  );
};
