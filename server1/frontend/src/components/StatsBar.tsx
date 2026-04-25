import React from 'react';
import '../styles/global.css';

interface StatItemProps {
  value: string;
  label: string;
}

const StatItem: React.FC<StatItemProps> = ({ value, label }) => (
  <div style={{ textAlign: 'center' }}>
    <div style={{
      fontSize: '28px',
      fontWeight: 800,
      background: 'var(--gradient-main)',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      marginBottom: '4px'
    }}>
      {value}
    </div>
    <div style={{
      fontSize: '13px',
      color: 'var(--text-light)',
      fontWeight: 600,
      textTransform: 'uppercase',
      letterSpacing: '0.5px'
    }}>
      {label}
    </div>
  </div>
);

export const StatsBar: React.FC = () => {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(4, 1fr)',
      gap: '24px',
      backgroundColor: '#fff',
      padding: '32px 48px',
      borderRadius: 'var(--radius-lg)',
      boxShadow: 'var(--shadow-soft)',
      marginTop: '40px',
      backgroundImage: 'linear-gradient(to right, rgba(155, 81, 224, 0.05), rgba(47, 128, 237, 0.05))'
    }}>
      <StatItem value="285M+" label="Images Analyzed" />
      <StatItem value="75M+" label="Hazards Avoided" />
      <StatItem value="1.3B+" label="Interactions" />
      <StatItem value="100%" label="Commitment" />
    </div>
  );
};
