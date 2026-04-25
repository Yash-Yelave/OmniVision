import React from 'react';
import '../styles/global.css';

type TabId = 'gesture' | 'audio';

interface TabsProps {
  activeTab: TabId;
  setActiveTab: (tab: TabId) => void;
}

export const Tabs: React.FC<TabsProps> = ({ activeTab, setActiveTab }) => {
  const tabs: { id: TabId; label: string }[] = [
    { id: 'audio', label: 'Audio Assistant' },
    { id: 'gesture', label: 'Gesture Recognition' }
  ];

  return (
    <div style={{
      display: 'flex',
      backgroundColor: '#f3f4f6',
      padding: '8px',
      borderRadius: 'var(--radius-full)',
      width: '100%',
      maxWidth: '700px', // Medium Manageable Desktop Size
      margin: '0 auto 48px auto',
    }}>
      {tabs.map((tab) => {
        const isActive = activeTab === tab.id;
        return (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              flex: 1,
              padding: '18px 32px',
              borderRadius: 'var(--radius-full)',
              fontWeight: 700,
              fontSize: '18px',
              color: isActive ? '#fff' : 'var(--text-light)',
              background: isActive ? 'var(--primary)' : 'transparent',
              transition: 'var(--transition)'
            }}
          >
            {tab.label}
          </button>
        );
      })}
    </div>
  );
};
