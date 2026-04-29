import os
import io
import time
import uuid
import base64
import asyncio
from typing import Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import httpx

app = FastAPI(title="Server 2: ML Compute Engine (Heavy Compute)")

# Explicit CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global State & AI Initialization ---
general_yolo = None
pothole_yolo = None

# Cooldown dictionary: mapping connection IDs to the last timestamp a hazard was reported
cooldowns: Dict[str, float] = {}

@app.on_event("startup")
async def startup_event():
    global general_yolo, pothole_yolo
    print("[INIT] Loading YOLO models into memory...")
    try:
        general_yolo = YOLO('yolov8n.pt')
        print("[INIT] general_yolo (COCO) loaded successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to load general_yolo: {e}")
        
    try:
        if os.path.exists('pothole_yolo.pt'):
            pothole_yolo = YOLO('pothole_yolo.pt')
            print("[INIT] pothole_yolo loaded successfully.")
        else:
            print("[WARN] pothole_yolo.pt not found. Using general_yolo as fallback for now.")
            pothole_yolo = general_yolo
    except Exception as e:
        print(f"[ERROR] Failed to load pothole_yolo: {e}")

async def run_llava(base64_image: str, hazards: list) -> str:
    """Sends image to local Ollama API."""
    hazards_str = ", ".join(hazards)
    prompt = (
        f"The following objects were detected: [{hazards_str}]. "
        "Describe the immediate hazards in one short, concise sentence. "
        "Maximum 10 words. Do not use filler words."
    )
    
    payload = {
        "model": "llava:v1.6",
        "prompt": prompt,
        "images": [base64_image],
        "stream": False,
        "options": {
            "temperature": 0.2,
            "top_k": 40
        }
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post('http://localhost:11434/api/generate', json=payload, timeout=60.0)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
    except Exception as e:
        print(f"[Ollama Error] {e}")
        return "Error analyzing scene."

@app.websocket("/internal/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    conn_id = str(uuid.uuid4())
    print(f"[WS] Client connected: {conn_id}")
    
    try:
        while True:
            # Receive incoming frame bytes from Server 1
            frame_bytes = await websocket.receive_bytes()
            
            # Temporary file to process with YOLO
            temp_path = f"temp_frame_{conn_id}.jpg"
            with open(temp_path, "wb") as f:
                f.write(frame_bytes)
                
            detected_hazards = []
            try:
                # Logic Gate: Run the frame through both YOLO models
                if general_yolo:
                    results = general_yolo(temp_path, verbose=False)
                    for r in results:
                        for box in r.boxes:
                            cls_id = int(box.cls[0])
                            detected_hazards.append(general_yolo.names[cls_id])
                
                if pothole_yolo and pothole_yolo != general_yolo:
                    p_results = pothole_yolo(temp_path, verbose=False)
                    for r in p_results:
                        for box in r.boxes:
                            cls_id = int(box.cls[0])
                            detected_hazards.append(pothole_yolo.names[cls_id])
                elif pothole_yolo == general_yolo:
                    pass # Already ran general_yolo
                    
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            
            unique_hazards = list(set(detected_hazards))
            
            # Logic Gate: If no hazards are detected, silently drop the frame
            if not unique_hazards:
                continue
                
            # Cooldown Mechanism
            current_time = time.time()
            last_warn_time = cooldowns.get(conn_id, 0)
            
            if (current_time - last_warn_time) < 5.0:
                # If the user was warned less than 5 seconds ago, drop the frame
                continue
                
            # If clear, proceed and update the timestamp
            cooldowns[conn_id] = current_time
            
            # LLM Trigger
            print(f"[WS] {conn_id}: Hazards detected: {unique_hazards}. Triggering LLaVA...")
            base64_image = base64.b64encode(frame_bytes).decode('utf-8')
            llava_response = await run_llava(base64_image, unique_hazards)
            print(f"[WS] {conn_id}: LLaVA output: {llava_response}")
            
            # Response: Package YOLO labels, LLaVA text, and TTS URL
            payload = {
                "labels": unique_hazards,
                "llava_text": llava_response,
                "audio_url": "PLACEHOLDER_TTS_AUDIO_URL"
            }
            
            await websocket.send_json(payload)
            
    except WebSocketDisconnect:
        print(f"[WS] Client disconnected: {conn_id}")
        if conn_id in cooldowns:
            del cooldowns[conn_id]
    except Exception as e:
        print(f"[WS] Error: {e}")
        if conn_id in cooldowns:
            del cooldowns[conn_id]
