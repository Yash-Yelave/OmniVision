import React from 'react';
import { Eye, Users } from 'lucide-react';
import '../styles/global.css';

export const Navbar: React.FC = () => {
  return (
    <header style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '32px 0 40px 0',
      borderBottom: '1px solid #e5e7eb'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
        <div style={{
          background: 'var(--gradient-main)',
          padding: '16px',
          borderRadius: 'var(--radius-lg)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 8px 16px rgba(155, 81, 224, 0.25)'
        }}>
          <Eye size={40} color="#fff" strokeWidth={2.5} />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <h1 style={{ fontSize: '32px', fontWeight: 800, margin: 0, color: 'var(--text-dark)' }}>OmniVision</h1>
            <span style={{
              width: '12px',
              height: '12px',
              backgroundColor: '#10b981',
              borderRadius: '50%',
              display: 'inline-block',
              boxShadow: '0 0 8px rgba(16, 185, 129, 0.6)'
            }}></span>
          </div>
          <p style={{ color: 'var(--text-light)', fontSize: '18px', margin: '4px 0 0 0', fontWeight: 500 }}>AI-Powered Accessibility Assistant</p>
        </div>
      </div>
      
      <div style={{
        backgroundColor: '#f3f4f6',
        padding: '12px 24px',
        borderRadius: 'var(--radius-full)',
        display: 'flex',
        alignItems: 'center',
        gap: '16px',
        boxShadow: 'var(--shadow-soft)'
      }}>
        <div style={{
          backgroundColor: '#fff',
          width: '40px',
          height: '40px',
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 2px 6px rgba(0,0,0,0.08)'
        }}>
          <Users size={20} color="var(--primary)" />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <span style={{ fontSize: '14px', color: 'var(--text-light)', fontWeight: 600, letterSpacing: '0.5px', textTransform: 'uppercase' }}>Active Users</span>
          <span style={{ fontSize: '20px', fontWeight: 800, lineHeight: 1.2, color: 'var(--text-dark)' }}>1,416</span>
        </div>
      </div>
    </header>
  );
};
