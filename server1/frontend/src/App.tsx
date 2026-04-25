import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Tabs } from './components/Tabs';
import { GesturePage } from './pages/GesturePage';
import { AudioPage } from './pages/AudioPage';

type TabId = 'gesture' | 'audio';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabId>('audio');

  return (
    <div className="app-container">
      <Navbar />
      <main>
        <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
        <div style={{ marginTop: '24px', paddingBottom: '60px' }}>
          {activeTab === 'gesture' && <GesturePage />}
          {activeTab === 'audio' && <AudioPage />}
        </div>
      </main>
    </div>
  );
};

export default App;
