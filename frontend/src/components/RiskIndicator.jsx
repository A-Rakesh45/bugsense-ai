import React from 'react';

export const RiskIndicator = ({ score = 0, level = 'Low' }) => {
  let barColor = '#10b981'; // Green
  if (score >= 86) barColor = '#ef4444'; // Red
  else if (score >= 66) barColor = '#f59e0b'; // Amber
  else if (score >= 36) barColor = '#2563eb'; // Blue

  return (
    <div style={{ width: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
        <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>
          Overall Risk Score
        </span>
        <span style={{ fontSize: '13px', fontWeight: 700, color: barColor }}>
          {score} / 100 ({level})
        </span>
      </div>
      <div style={{
        height: '8px',
        width: '100%',
        backgroundColor: '#e2e8f0',
        borderRadius: '4px',
        overflow: 'hidden'
      }}>
        <div style={{
          height: '100%',
          width: `${Math.min(100, Math.max(0, score))}%`,
          backgroundColor: barColor,
          borderRadius: '4px',
          transition: 'width 0.3s ease'
        }} />
      </div>
    </div>
  );
};
