import React, { useState } from 'react';
import { Camera, Play, MapPin, Users, Brain, AlertTriangle, Watch, WifiOff, Image as ImageIcon } from 'lucide-react';
import { StatsBar } from '../components/StatsBar';
import { FeatureCard } from '../components/FeatureCard';

export const ImageDescriptionPage: React.FC = () => {
  const [activeLang, setActiveLang] = useState('English');
  const [speed, setSpeed] = useState('1.0x');

  const languages = ['English', 'हिंदी', 'मराठी'];
  const speeds = ['0.75x', '1.0x', '1.25x'];

  const features = [
    {
      title: 'Crowdsourced Accessibility Map',
      description: 'Navigate your city with real-time accessibility data shared by the community.',
      tag: 'Navigation',
      icon: <MapPin />,
      tagColor: '#3b82f6'
    },
    {
      title: 'Real-time Volunteer Network',
      description: 'Connect instantly with verified volunteers for remote visual assistance.',
      tag: 'Community',
      icon: <Users />,
      tagColor: '#10b981'
    },
    {
      title: 'Personalized AI Learning',
      description: 'The AI adapts to your specific needs and environment over time.',
      tag: 'AI/ML',
      icon: <Brain />,
      tagColor: '#8b5cf6'
    },
    {
      title: 'Predictive Hazard Alerts',
      description: 'Get warned about potential obstacles and hazards before you reach them.',
      tag: 'Safety',
      icon: <AlertTriangle />,
      tagColor: '#f59e0b'
    },
    {
      title: 'Smartwatch Integration',
      description: 'Receive haptic feedback and discreet audio cues directly on your wrist.',
      tag: 'Hardware',
      icon: <Watch />,
      tagColor: '#ec4899'
    },
    {
      title: 'Offline Mode with Caching',
      description: 'Core detection features remain available even without an internet connection.',
      tag: 'Performance',
      icon: <WifiOff />,
      tagColor: '#6366f1'
    }
  ];

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      {/* Top Controls */}
      <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: '16px' }}>
        <div style={{ display: 'flex', backgroundColor: '#fff', borderRadius: 'var(--radius-full)', padding: '4px', boxShadow: 'var(--shadow-soft)' }}>
          {languages.map(lang => (
            <button
              key={lang}
              onClick={() => setActiveLang(lang)}
              style={{
                padding: '6px 16px',
                borderRadius: 'var(--radius-full)',
                fontSize: '13px',
                fontWeight: 600,
                backgroundColor: activeLang === lang ? 'var(--text-dark)' : 'transparent',
                color: activeLang === lang ? '#fff' : 'var(--text-light)',
              }}
            >
              {lang}
            </button>
          ))}
        </div>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          backgroundColor: '#fff',
          padding: '8px 16px',
          borderRadius: 'var(--radius-full)',
          boxShadow: 'var(--shadow-soft)',
          fontSize: '13px',
          fontWeight: 600,
          color: 'var(--text-dark)'
        }}>
          <span style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: '#f59e0b' }}></span>
          Standby
        </div>
      </div>

      {/* Main Layout */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 380px', gap: '24px' }}>
        
        {/* Left Camera Preview */}
        <div style={{
          backgroundColor: '#111827',
          borderRadius: 'var(--radius-lg)',
          minHeight: '480px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative',
          overflow: 'hidden',
          boxShadow: 'var(--shadow-soft)'
        }}>
          <div style={{
            width: '80px',
            height: '80px',
            borderRadius: '50%',
            backgroundColor: 'rgba(255,255,255,0.1)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '24px'
          }}>
            <Camera size={36} color="#ffffff" opacity={0.8} />
          </div>
          
          <button style={{
            position: 'absolute',
            bottom: '32px',
            background: 'var(--gradient-main)',
            color: '#fff',
            padding: '14px 32px',
            borderRadius: 'var(--radius-full)',
            fontWeight: 600,
            fontSize: '16px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            boxShadow: '0 8px 16px rgba(139, 92, 246, 0.3)'
          }}>
            <Camera size={20} />
            Start Detection
          </button>
        </div>

        {/* Right Stacked Cards */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          
          {/* Scene Description Card */}
          <div className="card-shadow" style={{
            backgroundColor: '#fff',
            borderRadius: 'var(--radius-lg)',
            padding: '24px',
            flex: 1
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
              <div style={{ padding: '8px', backgroundColor: '#f3f4f6', borderRadius: '8px', color: 'var(--primary)' }}>
                <ImageIcon size={20} />
              </div>
              <h2 style={{ fontSize: '18px', fontWeight: 700, margin: 0 }}>Scene Description</h2>
            </div>
            <div style={{
              backgroundColor: '#f9fafb',
              borderRadius: '8px',
              padding: '24px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--text-light)',
              minHeight: '120px',
              textAlign: 'center',
              border: '1px dashed #e5e7eb'
            }}>
              Start camera to see description
            </div>
          </div>

          {/* Audio Output Card */}
          <div className="card-shadow" style={{
            backgroundColor: '#fff',
            borderRadius: 'var(--radius-lg)',
            padding: '24px'
          }}>
            <h2 style={{ fontSize: '16px', fontWeight: 700, marginBottom: '16px', color: 'var(--text-dark)' }}>
              Audio Output
            </h2>
            
            <button style={{
              width: '100%',
              background: 'var(--gradient-main)',
              color: '#fff',
              padding: '12px',
              borderRadius: 'var(--radius-md)',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              marginBottom: '20px'
            }}>
              <Play fill="#fff" size={18} />
              Play Description
            </button>

            <div style={{ marginBottom: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: 'var(--text-light)', marginBottom: '8px' }}>
                <span>0:00</span>
                <span>0:00</span>
              </div>
              <div style={{ height: '6px', backgroundColor: '#f3f4f6', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: '0%', height: '100%', backgroundColor: 'var(--primary)' }}></div>
              </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-light)' }}>Speed</span>
              <div style={{ display: 'flex', gap: '4px', backgroundColor: '#f3f4f6', padding: '4px', borderRadius: '6px' }}>
                {speeds.map(s => (
                  <button
                    key={s}
                    onClick={() => setSpeed(s)}
                    style={{
                      padding: '4px 10px',
                      borderRadius: '4px',
                      fontSize: '12px',
                      fontWeight: 600,
                      backgroundColor: speed === s ? '#fff' : 'transparent',
                      color: speed === s ? 'var(--primary)' : 'var(--text-light)',
                      boxShadow: speed === s ? '0 1px 2px rgba(0,0,0,0.1)' : 'none'
                    }}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Suggested Features Section */}
      <div style={{ marginTop: '48px' }}>
        <div style={{ marginBottom: '24px' }}>
          <h2 style={{ fontSize: '24px', fontWeight: 800, color: 'var(--text-dark)', marginBottom: '8px' }}>
            Suggested Features & Enhancements
          </h2>
          <p style={{ color: 'var(--text-light)', fontSize: '15px' }}>
            Discover powerful tools designed to expand OmniVision's capabilities.
          </p>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '24px'
        }}>
          {features.map(f => (
            <FeatureCard key={f.title} {...f} />
          ))}
        </div>

        <StatsBar />
      </div>

    </div>
  );
};
