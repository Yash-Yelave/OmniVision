import React, { useState, useRef, useEffect } from 'react';
import { Mic, Send, Activity } from 'lucide-react';
import { analyzeImage, sendChat, BASE_URL } from '../api/server1';
import '../styles/global.css';

declare global {
  interface Window {
    SpeechRecognition: any;
    webkitSpeechRecognition: any;
  }
}

export const AudioPage: React.FC = () => {
  const [currentLang, setCurrentLang] = useState<'en'|'hi'|'mr'>('en');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [responseText, setResponseText] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);
  
  const recognitionRef = useRef<any>(null);

  // Reference to hold the video stream so we can stop it
  const streamRef = useRef<MediaStream | null>(null);
  const isTrackingRef = useRef<boolean>(false);

  useEffect(() => {
    // SpeechRecognition removed to prevent network errors
  }, []);

  const toggleTracking = () => {
    if (isTrackingRef.current) {
      // Stop tracking
      isTrackingRef.current = false;
      setIsListening(false);
      setResponseText("Tracking stopped. Tap to resume.");
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
        streamRef.current = null;
      }
    } else {
      // Start tracking
      isTrackingRef.current = true;
      setIsListening(true);
      captureAndAnalyzeLoop();
    }
  };

  const speak = (text: string, callback?: () => void) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      if (currentLang === 'hi') utterance.lang = 'hi-IN';
      else if (currentLang === 'mr') utterance.lang = 'mr-IN';
      else utterance.lang = 'en-US';
      
      utterance.onend = () => {
        if (callback) {
          callback();
        } else {
          // Continuous Mode: Auto-start listening after reading output
          setTimeout(() => {
            startListening();
          }, 800);
        }
      };
      
      window.speechSynthesis.speak(utterance);
    } else {
      if (callback) {
        callback();
      } else {
        setTimeout(() => startListening(), 800);
      }
    }
  };

  const captureAndAnalyzeLoop = async () => {
    setResponseText("Initializing continuous tracker...");
    setIsProcessing(true);
    
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
      streamRef.current = stream;
      const video = document.createElement('video');
      video.srcObject = stream;
      
      await new Promise((resolve) => {
        video.onloadedmetadata = () => {
          video.play();
          resolve(true);
        };
      });

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      setIsProcessing(false);
      setResponseText("Tracking active. Analyzing...");

      const processFrame = async () => {
        if (!isTrackingRef.current) return;
        
        ctx?.drawImage(video, 0, 0);

        canvas.toBlob(async (blob) => {
          if (!blob || !isTrackingRef.current) return;

          try {
            const result = await analyzeImage(blob);
            
            if (result.status === "success" && result.data?.text) {
              const text = result.data.text;
              setResponseText(text);
              speak(text);
            }
          } catch (apiError) {
            console.error("Analyze API error:", apiError);
            if (isTrackingRef.current) setResponseText("Connecting to Server 2...");
          }
          
          // Buffer System: Wait for speech to finish before taking the next picture!
          if (isTrackingRef.current) {
            const scheduleNext = () => {
              if (!isTrackingRef.current) return;
              if (window.speechSynthesis.speaking) {
                setTimeout(scheduleNext, 500); // Wait another half second if still talking
              } else {
                setTimeout(processFrame, 1000); // 1 second breath after talking before next scan
              }
            };
            scheduleNext();
          }
        }, 'image/jpeg', 0.5);
      };

      // Start the recursive loop
      processFrame();

    } catch (err) {
      console.error("Camera error:", err);
      setIsProcessing(false);
      setIsListening(false);
      isTrackingRef.current = false;
      setResponseText("Failed to access camera.");
    }
  };

  const handleUserText = async (text: string) => {
    if (!text.trim()) return;
    setIsProcessing(true);
    setResponseText(`Thinking about: "${text}"...`);
    
    try {
      const result = await sendChat(text);
      
      if (result.status === "success") {
        if (result.action === "TRIGGER_CAMERA") {
          const ackText = result.data.text || "Scanning the environment now.";
          setResponseText(ackText);
          speak(ackText, () => {
             captureAndAnalyze();
          });
        } else if (result.action === "SPEAK") {
          setResponseText(result.data.text);
          speak(result.data.text);
          setIsProcessing(false);
        }
      } else {
        setResponseText("Error processing request.");
        setIsProcessing(false);
      }
    } catch (err) {
      console.error(err);
      setResponseText("Server unreachable.");
      setIsProcessing(false);
    }
  };


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
          <div 
            onClick={!isProcessing ? toggleTracking : undefined}
            style={{
            position: 'relative',
            width: '240px',
            height: '240px',
            borderRadius: '50%',
            backgroundColor: isProcessing ? '#9ca3af' : (isListening ? '#ef4444' : 'var(--primary)'),
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: isProcessing ? 'none' : (isListening ? '0 20px 45px rgba(239, 68, 68, 0.4)' : '0 20px 45px rgba(155, 81, 224, 0.3)'),
            cursor: isProcessing ? 'not-allowed' : 'pointer',
            transition: 'all 0.2s ease',
            zIndex: 10
          }}>
            {isProcessing ? <Activity size={96} color="#ffffff" className="animate-spin" /> : <Activity size={96} color="#ffffff" strokeWidth={2} />}
            
            {/* Aura Outline */}
            <div style={{
              position: 'absolute',
              top: '-12%', left: '-12%', right: '-12%', bottom: '-12%',
              borderRadius: '50%',
              backgroundColor: isProcessing ? 'transparent' : (isListening ? 'rgba(239, 68, 68, 0.15)' : 'rgba(155, 81, 224, 0.1)'),
              zIndex: -1,
              transition: 'all 0.2s ease',
              animation: isListening ? 'pulse 1.5s infinite' : 'none'
            }}></div>
          </div>
          
          <h3 style={{ fontSize: '40px', fontWeight: 800, color: 'var(--text-dark)', margin: 0, textAlign: 'center', maxWidth: '800px' }}>
            {responseText || "Tap to Start Tracking"}
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
            ref={inputRef}
            type="text" 
            placeholder="Type your question or use the mic..." 
            onKeyDown={(e) => {
              if (e.key === 'Enter' && inputRef.current?.value) {
                 handleUserText(inputRef.current.value);
                 inputRef.current.value = "";
              }
            }}
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
          
          <button 
            onClick={() => {
              if (inputRef.current?.value) {
                handleUserText(inputRef.current.value);
                inputRef.current.value = "";
              }
            }}
            style={{
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
