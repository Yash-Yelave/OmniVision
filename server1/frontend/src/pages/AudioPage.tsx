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

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      
      recognitionRef.current.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setResponseText(`You: "${transcript}"`);
        setIsListening(false);
        handleUserText(transcript);
      };
      
      recognitionRef.current.onerror = (event: any) => {
        console.error("Speech recognition error:", event.error);
        setIsListening(false);
        if (event.error === 'not-allowed') {
          setResponseText("Microphone access denied or insecure connection. (HTTPS required on mobile).");
        } else if (event.error === 'network') {
          setResponseText("Network error during speech recognition.");
        } else if (event.error === 'no-speech') {
          setResponseText("No speech detected. Please try again.");
        } else {
          setResponseText(`Speech error: ${event.error}. Try again.`);
        }
      };
      
      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
      
    } else {
      setResponseText("Speech recognition not supported in this browser.");
    }
  }, []);

  const startListening = () => {
    if (recognitionRef.current && !isProcessing) {
      if (currentLang === 'hi') recognitionRef.current.lang = 'hi-IN';
      else if (currentLang === 'mr') recognitionRef.current.lang = 'mr-IN';
      else recognitionRef.current.lang = 'en-US';
      
      try {
        recognitionRef.current.start();
        setIsListening(true);
        setResponseText("Listening...");
      } catch (err) {
        console.error("Could not start recognition", err);
      }
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

  const captureAndAnalyze = async () => {
    setIsProcessing(true);
    setResponseText((prev) => prev || "Connecting to continuous video stream...");
    
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
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

      // Open WebSocket connection to the Gateway (Server 1 -> Server 2)
      // Extract the hostname from BASE_URL to ensure mobile devices don't try to connect to their own localhost
      const wsHost = new URL(BASE_URL).hostname;
      const ws = new WebSocket(`ws://${wsHost}:8002/api/stream`);
      
      ws.onopen = () => {
        setResponseText("Streaming to Server 2...");
        setIsProcessing(false);
        
        // Start sending frames continuously every 2 seconds
        setInterval(() => {
          ctx?.drawImage(video, 0, 0);
          canvas.toBlob((blob) => {
            if (blob && ws.readyState === WebSocket.OPEN) {
              ws.send(blob);
            }
          }, 'image/jpeg', 0.5);
        }, 2000);
      };

      ws.onmessage = (event) => {
        try {
          const result = JSON.parse(event.data);
          if (result.text) {
             setResponseText(result.text);
             // Only speak if not currently speaking to avoid overlapping chaos
             if (!window.speechSynthesis.speaking) {
                speak(result.text);
             }
          }
        } catch (e) {
          console.error("Invalid WS JSON", e);
        }
      };

      ws.onerror = (error) => {
        console.error("WebSocket Error:", error);
        setResponseText("Streaming error. Is gateway.py running on 8002?");
        setIsProcessing(false);
      };
      
      ws.onclose = () => {
        console.log("WebSocket stream closed.");
        stream.getTracks().forEach(track => track.stop());
      };

    } catch (err) {
      console.error("Camera error:", err);
      setIsProcessing(false);
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

  const toggleListening = () => {
    if (isProcessing) return;
    
    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
      setResponseText("");
    } else {
      if (recognitionRef.current) {
        startListening();
      } else {
        setResponseText("Speech recognition not supported in this browser.");
      }
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
            onClick={!isProcessing ? toggleListening : undefined}
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
            {isProcessing ? <Activity size={96} color="#ffffff" className="animate-spin" /> : <Mic size={96} color="#ffffff" strokeWidth={2} />}
            
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
            {responseText || "Tap to speak with OmniVision"}
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
