import React from 'react';
import '../styles/global.css';

interface FeatureCardProps {
  title: string;
  description: string;
  tag: string;
  icon: React.ReactNode;
  tagColor: string;
}

export const FeatureCard: React.FC<FeatureCardProps> = ({ title, description, tag, icon, tagColor }) => {
  return (
    <div className="card-shadow" style={{
      backgroundColor: '#fff',
      padding: '24px',
      borderRadius: 'var(--radius-lg)',
      display: 'flex',
      flexDirection: 'column',
      gap: '16px',
      transition: 'var(--transition)',
      border: '1px solid #f3f4f6'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div style={{
          width: '48px',
          height: '48px',
          borderRadius: '12px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: `${tagColor}20`,
          color: tagColor
        }}>
          {icon}
        </div>
        <span style={{
          fontSize: '12px',
          fontWeight: 600,
          padding: '4px 10px',
          borderRadius: 'var(--radius-full)',
          backgroundColor: `${tagColor}15`,
          color: tagColor
        }}>
          {tag}
        </span>
      </div>
      
      <div>
        <h3 style={{ fontSize: '18px', fontWeight: 700, marginBottom: '8px', color: 'var(--text-dark)' }}>
          {title}
        </h3>
        <p style={{ fontSize: '14px', color: 'var(--text-light)', lineHeight: 1.5 }}>
          {description}
        </p>
      </div>
      
      <button style={{
        marginTop: 'auto',
        textAlign: 'left',
        color: 'var(--primary)',
        fontWeight: 600,
        fontSize: '14px',
        display: 'flex',
        alignItems: 'center',
        gap: '4px'
      }}>
        Learn more &rarr;
      </button>
    </div>
  );
};
