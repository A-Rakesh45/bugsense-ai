import React from 'react';

export const StatusBadge = ({ type = 'severity', value }) => {
  if (!value) return null;

  let badgeClass = 'badge ';
  const val = strClean(value);

  if (type === 'severity') {
    if (val === 'critical') badgeClass += 'badge-critical';
    else if (val === 'high') badgeClass += 'badge-high';
    else if (val === 'medium') badgeClass += 'badge-medium';
    else badgeClass += 'badge-low';
  } else if (type === 'priority') {
    if (val === 'p1') badgeClass += 'badge-critical';
    else if (val === 'p2') badgeClass += 'badge-high';
    else if (val === 'p3') badgeClass += 'badge-medium';
    else badgeClass += 'badge-low';
  } else if (type === 'status') {
    if (val === 'open') badgeClass += 'badge-open';
    else if (val === 'in progress') badgeClass += 'badge-progress';
    else if (val === 'resolved') badgeClass += 'badge-resolved';
    else badgeClass += 'badge-closed';
  }

  return (
    <span className={badgeClass}>
      {value}
    </span>
  );
};

function strClean(str) {
  return String(str || '').trim().toLowerCase();
}
