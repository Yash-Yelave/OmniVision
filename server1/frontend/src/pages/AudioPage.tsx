import React, { useState } from 'react';
import { Mic, Send } from 'lucide-react';
import '../styles/global.css';

export const AudioPage: React.FC = () => {
  const [currentLang, setCurrentLang] = useState<'en'|'hi'|'mr'>('en');

  return (
    <div className="animate-fade-in" style={{ 
      display: 'flex', 
      justifyContent: 'center',
      padding: '24px 0 60px 0'
    }}>
      <div className="card-shadow" style={{
        backgroundColor: '#fff',
        borderRadius: 'var(--radius-lg)',
        padding: '64px 80px',
        maxWidth: '1000px',
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '48px'
      }}>
        
        {/* Header */}
        <div style={{ width: '100%', textAlign: 'left' }}>
          <h2 style={{ fontSize: '40px', fontWeight: 800, margin: '0 0 12px 0', color: 'var(--text-dark)' }}>Voice Assistant</h2>
          <p style={{ color: 'var(--text-light)', fontSize: '20px', margin: 0, fontWeight: 500 }}>Ask questions using your voice</p>
        </div>

        {/* Language Segmented Control */}
        <div style={{
          display: 'flex',
          width: '100%',
          backgroundColor: '#f3f4f6',
          borderRadius: 'var(--radius-full)',
          padding: '8px'
        }}>
          {[
            { id: 'en', label: 'English' },
            { id: 'hi', label: 'हिंदी' },
            { id: 'mr', label: 'मराठी' }
          ].map(lang => (
            <button
              key={lang.id}
              onClick={() => setCurrentLang(lang.id as any)}
              style={{
                flex: 1,
                padding: '18px 0',
                borderRadius: 'var(--radius-full)',
                fontSize: '20px',
                fontWeight: 700,
                backgroundColor: currentLang === lang.id ? '#fff' : 'transparent',
                color: currentLang === lang.id ? 'var(--primary)' : 'var(--text-light)',
                boxShadow: currentLang === lang.id ? '0 4px 8px rgba(0,0,0,0.05)' : 'none',
                border: 'none',
                cursor: 'pointer',
                transition: 'var(--transition)'
              }}
            >
              {lang.label}
            </button>
          ))}
        </div>

        {/* Big Mic Button */}
        <div style={{
          margin: '32px 0',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '56px'
        }}>
          <div style={{
            position: 'relative',
            width: '240px',
            height: '240px',
            borderRadius: '50%',
            backgroundColor: 'var(--primary)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 20px 45px rgba(155, 81, 224, 0.3)',
            cursor: 'pointer',
            transition: 'transform 0.2s ease',
            zIndex: 10
          }}>
            <Mic size={96} color="#ffffff" strokeWidth={2} />
            
            {/* Soft Purple Aura Outline */}
            <div style={{
              position: 'absolute',
              top: '-12%', left: '-12%', right: '-12%', bottom: '-12%',
              borderRadius: '50%',
              backgroundColor: 'rgba(155, 81, 224, 0.1)',
              zIndex: -1
            }}></div>
          </div>
          
          <h3 style={{ fontSize: '40px', fontWeight: 800, color: 'var(--text-dark)', margin: 0 }}>
            How can I help you?
          </h3>
        </div>

        {/* Bottom Input Field */}
        <div style={{ width: '100%', position: 'relative', marginTop: '16px' }}>
          <button style={{
            position: 'absolute',
            left: '20px',
            top: '50%',
            transform: 'translateY(-50%)',
            color: 'var(--primary)',
            padding: '12px',
            borderRadius: '50%',
            background: 'none',
            border: 'none',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Mic size={32} />
          </button>
          
          <input 
            type="text" 
            placeholder="Type your question or use the mic..." 
            style={{
              width: '100%',
              padding: '32px 100px 32px 80px',
              borderRadius: 'var(--radius-full)',
              border: '2px solid #e5e7eb',
              backgroundColor: '#fff',
              fontSize: '20px',
              fontWeight: 500,
              outline: 'none',
              boxShadow: '0 8px 30px rgba(0,0,0,0.04)',
              color: 'var(--text-dark)',
              fontFamily: 'inherit',
              transition: 'var(--transition)'
            }}
          />
          
          <button style={{
            position: 'absolute',
            right: '16px',
            top: '50%',
            transform: 'translateY(-50%)',
            backgroundColor: 'var(--primary)',
            color: '#fff',
            width: '64px',
            height: '64px',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: 'none',
            boxShadow: '0 8px 25px rgba(155, 81, 224, 0.3)',
            cursor: 'pointer',
            transition: 'var(--transition)'
          }}>
            <Send size={28} />
          </button>
        </div>

      </div>
    </div>
  );
};
