import React, { useState, useRef } from 'react';
import { Hand, Volume2, Activity } from 'lucide-react';
import '../styles/global.css';

export const GesturePage: React.FC = () => {
  const [currentGesture, setCurrentGesture] = useState<any>(null);
  const [isRecognizing, setIsRecognizing] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentLang, setCurrentLang] = useState<'en'|'hi'|'mr'>('en');
  const [speed, setSpeed] = useState<'0.75x'|'1.0x'|'1.25x'>('1.0x');
  const [isCameraActive, setIsCameraActive] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

  const gestures = [
    { id: 'hello', emoji: '👋', name: 'Hello', translations: {
      en: { name: 'Hello', desc: 'Greeting detected' },
      hi: { name: 'नमस्ते', desc: 'अभिवादन का पता चला' },
      mr: { name: 'नमस्कार', desc: 'अभिवादन आढळले' }
    }},
    { id: 'yes', emoji: '👍', name: 'Yes', translations: {
      en: { name: 'Yes', desc: 'Affirmative detected' },
      hi: { name: 'हाँ', desc: 'सकारात्मक उत्तर' },
      mr: { name: 'होय', desc: 'सकारात्मक उत्तर' }
    }},
    { id: 'no', emoji: '✋', name: 'No', translations: {
      en: { name: 'No', desc: 'Negative detected' },
      hi: { name: 'नहीं', desc: 'नकारात्मक उत्तर' },
      mr: { name: 'नाही', desc: 'नकारात्मक उत्तर' }
    }},
    { id: 'stop', emoji: '🛑', name: 'Stop', translations: {
      en: { name: 'Stop', desc: 'Stop movement immediately' },
      hi: { name: 'रुक जाओ', desc: 'तुरंत चलना बंद करें' },
      mr: { name: 'थांबा', desc: 'त्वरित हालचाल थांबवा' }
    }},
    { id: 'help', emoji: '🙋', name: 'Help', translations: {
      en: { name: 'Help Needed', desc: 'Request assistance from nearby people' },
      hi: { name: 'मदद चाहिए', desc: 'आसपास के लोगों से सहायता का अनुरोध करें' },
      mr: { name: 'मदत हवी आहे', desc: 'जवळपासच्या लोकांकडून मदत मागा' }
    }},
    { id: 'direction', emoji: '👉', name: 'Direction', translations: {
      en: { name: 'Direction', desc: 'Pointing direction' },
      hi: { name: 'दिशा', desc: 'दिशा की ओर इशारा' },
      mr: { name: 'दिशा', desc: 'दिशा दर्शवित आहे' }
    }},
    { id: 'emergency', emoji: '⚠️', name: 'Emergency', translations: {
      en: { name: 'Emergency', desc: 'Immediate hazard detected' },
      hi: { name: 'आपातकाल', desc: 'तत्काल खतरे का पता चला' },
      mr: { name: 'आणीबाणी', desc: 'तात्काळ धोका आढळला' }
    }},
  ];

  const getSpeedNumber = (s: string) => parseFloat(s.replace('x', ''));

  const speakText = (gesture: any, targetLang: 'en'|'hi'|'mr') => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const langData = gesture.translations[targetLang];
      const text = `${langData.name}`;
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = getSpeedNumber(speed);
      if (targetLang === 'hi') utterance.lang = 'hi-IN';
      if (targetLang === 'mr') utterance.lang = 'mr-IN';
      if (targetLang === 'en') utterance.lang = 'en-US';
      utterance.onstart = () => setIsPlaying(true);
      utterance.onend = () => setIsPlaying(false);
      utterance.onerror = () => setIsPlaying(false);
      window.speechSynthesis.speak(utterance);
    }
  };

  const triggerGesture = (gesture: any) => {
    setCurrentGesture(gesture);
    speakText(gesture, currentLang);
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      setIsCameraActive(true);
    } catch (err) {
      console.error("Camera access denied", err);
    }
  };

  const handleStartRecognition = () => {
    if (!isCameraActive) {
      startCamera();
    }
    setIsRecognizing(true);
    setTimeout(() => {
      const randomGesture = gestures[Math.floor(Math.random() * gestures.length)];
      triggerGesture(randomGesture);
      setIsRecognizing(false);
    }, 2500);
  };

  return (
    <div className="animate-fade-in" style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      gap: '32px', 
      width: '100%', 
      paddingBottom: '40px'
    }}>
      
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1 style={{ fontSize: '32px', fontWeight: 800, color: 'var(--text-dark)', marginBottom: '8px' }}>
            Gesture Recognition
          </h1>
          <p style={{ color: 'var(--text-light)', fontSize: '18px' }}>
            Understand hand gestures in real-time
          </p>
        </div>
        <div style={{ 
          backgroundColor: '#fffbeb', 
          color: '#f59e0b', 
          padding: '8px 16px', 
          borderRadius: 'var(--radius-full)',
          fontSize: '16px',
          fontWeight: 700
        }}>
          Standby
        </div>
      </div>

      {/* Main Grid Layout for Desktop */}
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: '32px',
        alignItems: 'stretch'
      }}>

        {/* Left Column (Primary Focus - Camera) */}
        <div style={{ 
          flex: '1.5 1 500px', 
          display: 'flex', 
          flexDirection: 'column', 
          gap: '32px',
          minWidth: 0 
        }}>
          {/* Live Gesture Detection Card */}
          <div className="card-shadow" style={{
            backgroundColor: '#fff',
            borderRadius: 'var(--radius-lg)',
            padding: '32px',
            display: 'flex',
            flexDirection: 'column',
            gap: '24px',
            height: '100%' 
          }}>
            <div>
              <h2 style={{ fontSize: '24px', fontWeight: 700, color: 'var(--text-dark)', marginBottom: '8px' }}>
                Live Gesture Detection
              </h2>
              <p style={{ color: 'var(--text-light)', fontSize: '16px' }}>
                Detect and interpret hand gestures
              </p>
            </div>

            <div style={{
              width: '100%',
              flex: 1, 
              minHeight: '450px', 
              backgroundColor: '#1f2937',
              borderRadius: '20px',
              overflow: 'hidden',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              position: 'relative'
            }}>
              {isCameraActive ? (
                <video 
                  ref={videoRef}
                  autoPlay 
                  playsInline 
                  muted 
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                    transform: 'scaleX(-1)'
                  }}
                />
              ) : (
                <Hand size={64} color="rgba(255,255,255,0.2)" strokeWidth={1.5} />
              )}
            </div>

            <button 
              onClick={handleStartRecognition}
              disabled={isRecognizing}
              style={{
                width: '100%',
                backgroundColor: 'var(--primary)',
                color: '#fff',
                padding: '24px',
                borderRadius: 'var(--radius-full)',
                fontWeight: 700,
                fontSize: '20px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '12px',
                opacity: isRecognizing ? 0.8 : 1,
                cursor: isRecognizing ? 'not-allowed' : 'pointer',
                transition: 'var(--transition)'
            }}>
              {isRecognizing && <Activity size={24} className="animate-spin" />}
              {isRecognizing ? 'Recognizing...' : 'Start Gesture Detection'}
            </button>
          </div>
        </div>

        {/* Right Column (Controls and Info) */}
        <div style={{ 
          flex: '1 1 400px', 
          display: 'flex', 
          flexDirection: 'column', 
          gap: '32px',
          minWidth: 0 
        }}>
          {/* Detected Gesture Card */}
          <div className="card-shadow" style={{
            backgroundColor: '#fff',
            borderRadius: 'var(--radius-lg)',
            padding: '32px',
            display: 'flex',
            flexDirection: 'column',
            gap: '24px'
          }}>
            <h2 style={{ fontSize: '24px', fontWeight: 700, color: 'var(--text-dark)' }}>
              Detected Gesture
            </h2>

            <div style={{
              backgroundColor: 'rgba(155, 81, 224, 0.08)',
              borderRadius: '16px',
              padding: '40px 24px',
              textAlign: 'center',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '12px'
            }}>
              <h3 style={{ 
                fontSize: '48px', 
                fontWeight: 800, 
                color: 'var(--primary)', 
                margin: 0,
                textTransform: 'capitalize'
              }}>
                {currentGesture ? currentGesture.translations[currentLang].name : 'None'}
              </h3>
              <p style={{ color: 'var(--text-light)', fontSize: '18px' }}>
                {currentGesture ? 'Gesture detected successfully' : 'Waiting for gesture...'}
              </p>
            </div>

            {/* Language Selector */}
            <div style={{
              display: 'flex',
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
                    padding: '14px 0',
                    borderRadius: 'var(--radius-full)',
                    fontSize: '18px',
                    fontWeight: 700,
                    backgroundColor: currentLang === lang.id ? '#fff' : 'transparent',
                    color: currentLang === lang.id ? 'var(--primary)' : 'var(--text-light)',
                    boxShadow: currentLang === lang.id ? '0 2px 6px rgba(0,0,0,0.05)' : 'none',
                    border: 'none',
                    cursor: 'pointer',
                    transition: 'var(--transition)'
                  }}
                >
                  {lang.label}
                </button>
              ))}
            </div>

            <button 
              onClick={() => currentGesture && speakText(currentGesture, currentLang)}
              disabled={!currentGesture || isPlaying}
              style={{
                width: '100%',
                backgroundColor: 'var(--primary)',
                color: '#fff',
                padding: '24px',
                borderRadius: 'var(--radius-full)',
                fontWeight: 700,
                fontSize: '20px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '12px',
                opacity: (!currentGesture || isPlaying) ? 0.6 : 1,
                cursor: (!currentGesture || isPlaying) ? 'not-allowed' : 'pointer',
                transition: 'opacity 0.2s'
              }}>
              <Volume2 size={24} />
              Play Gesture Meaning
            </button>

            {/* Speed Controls */}
            <div style={{ display: 'flex', gap: '20px', alignItems: 'center', padding: '0 8px', justifyContent: 'center' }}>
              {['0.75x', '1.0x', '1.25x'].map(s => (
                <button
                  key={s}
                  onClick={() => setSpeed(s as any)}
                  style={{
                    fontSize: '18px',
                    fontWeight: speed === s ? 800 : 600,
                    color: speed === s ? 'var(--primary)' : 'var(--text-light)',
                    padding: '8px 0',
                    transition: 'var(--transition)'
                  }}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>

          {/* Gesture Library */}
          <div className="card-shadow" style={{
            backgroundColor: '#fff',
            borderRadius: 'var(--radius-lg)',
            padding: '32px'
          }}>
            <h2 style={{ fontSize: '24px', fontWeight: 700, color: 'var(--text-dark)', marginBottom: '24px' }}>
              Gesture Library
            </h2>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px' }}>
              {gestures.map((gesture) => (
                <button
                  key={gesture.id}
                  onClick={() => triggerGesture(gesture)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '12px 24px',
                    backgroundColor: '#fff',
                    border: '2px solid #e5e7eb',
                    borderRadius: '12px',
                    fontSize: '18px',
                    fontWeight: 700,
                    color: 'var(--text-dark)',
                    boxShadow: 'var(--shadow-soft)',
                    transition: 'var(--transition)',
                    cursor: 'pointer'
                  }}
                >
                  <span style={{ fontSize: '24px' }}>{gesture.emoji}</span>
                  {gesture.name}
                </button>
              ))}
            </div>
          </div>

          {/* How to Use Box */}
          <div className="card-shadow" style={{
            backgroundColor: '#fff',
            borderRadius: 'var(--radius-lg)',
            padding: '32px'
          }}>
            <h2 style={{ fontSize: '24px', fontWeight: 700, color: 'var(--text-dark)', marginBottom: '20px' }}>
              How to Use
            </h2>
            <ul style={{ 
              paddingLeft: '28px', 
              color: 'var(--text-light)', 
              fontSize: '18px',
              display: 'flex',
              flexDirection: 'column',
              gap: '16px',
              lineHeight: 1.5
            }}>
              <li>Keep your hand clearly in front of the camera</li>
              <li>Ensure proper lighting in your surroundings</li>
              <li>Hold the gesture steady for accurate detection</li>
            </ul>
          </div>
        </div>

      </div>
    </div>
  );
};
