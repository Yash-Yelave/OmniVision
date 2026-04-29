import os
import io
import time
import uuid
import base64
import asyncio
from typing import Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.responses import JSONResponse
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

# Dictionaries to track timers per connection
cooldowns: Dict[str, float] = {}       # tracks last_hazard_time (5s)
scan_timers: Dict[str, float] = {}     # tracks last_scan_time (30s)

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

async def run_llava(base64_image: str, prompt: str) -> str:
    """Sends image to local Ollama API with a specific prompt."""
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

@app.post("/internal/full-pipeline")
async def full_pipeline(file: UploadFile = File(...)):
    """
    REST API endpoint for Server 1 one-off requests.
    """
    temp_path = f"temp_{uuid.uuid4()}_{file.filename}"
    
    try:
        frame_bytes = await file.read()
        with open(temp_path, "wb") as f:
            f.write(frame_bytes)
            
        detected_hazards = []
        
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
                    
        unique_hazards = list(set(detected_hazards))
        
        hazards_str = ", ".join(unique_hazards) if unique_hazards else "none"
        prompt = (
            f"The following objects were detected: [{hazards_str}]. "
            "Describe the immediate hazards in one short, concise sentence. "
            "Maximum 10 words. Do not use filler words."
        )
        
        base64_image = base64.b64encode(frame_bytes).decode('utf-8')
        description = await run_llava(base64_image, prompt)
        
        return JSONResponse(content={"text": description})
        
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.websocket("/internal/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    conn_id = str(uuid.uuid4())
    print(f"[WS] Client connected: {conn_id}")
    
    # Initialize timers for this connection
    cooldowns[conn_id] = 0.0     # last_hazard_time
    scan_timers[conn_id] = 0.0   # last_scan_time
    
    try:
        while True:
            frame_bytes = await websocket.receive_bytes()
            current_time = time.time()
            
            # --- Path 3: The Periodic Scan (30 seconds) ---
            if (current_time - scan_timers[conn_id]) >= 30.0:
                print(f"[WS] {conn_id}: 30-second scan triggered. Bypassing YOLO...")
                scan_timers[conn_id] = current_time
                
                prompt = "Describe the general path ahead. Are there any stairs, ladders, drop-offs, or changes in elevation? One short sentence only."
                base64_image = base64.b64encode(frame_bytes).decode('utf-8')
                
                # We trigger LLaVA asynchronously but await it. 
                # Note: if LLaVA takes 3s, the loop will pause, but that's standard for this design
                # as long as the client isn't dropping the connection.
                llava_response = await run_llava(base64_image, prompt)
                print(f"[WS] {conn_id}: Periodic Scan Output: {llava_response}")
                
                payload = {
                    "labels": ["PERIODIC_SCAN"],
                    "llava_text": llava_response,
                    "audio_url": "PLACEHOLDER_TTS_AUDIO_URL"
                }
                
                await websocket.send_json(payload)
                continue # Skip YOLO processing for this frame
                
            # --- Standard YOLO Hazard Logic ---
            temp_path = f"temp_frame_{conn_id}.jpg"
            with open(temp_path, "wb") as f:
                f.write(frame_bytes)
                
            detected_hazards = []
            try:
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
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            
            unique_hazards = list(set(detected_hazards))
            
            # If no hazards are detected, drop the frame
            if not unique_hazards:
                continue
                
            # 5-second Cooldown check (last_hazard_time)
            last_hazard_time = cooldowns[conn_id]
            if (current_time - last_hazard_time) < 5.0:
                continue
                
            cooldowns[conn_id] = current_time
            
            print(f"[WS] {conn_id}: Hazards detected: {unique_hazards}. Triggering LLaVA...")
            base64_image = base64.b64encode(frame_bytes).decode('utf-8')
            
            hazard_prompt = "Describe this hazard in one short sentence."
            llava_response = await run_llava(base64_image, hazard_prompt)
            print(f"[WS] {conn_id}: Hazard Output: {llava_response}")
            
            payload = {
                "labels": unique_hazards,
                "llava_text": llava_response,
                "audio_url": "PLACEHOLDER_TTS_AUDIO_URL"
            }
            
            await websocket.send_json(payload)
            
    except WebSocketDisconnect:
        print(f"[WS] Client disconnected: {conn_id}")
    except Exception as e:
        print(f"[WS] Error: {e}")
    finally:
        # Clean up timers
        if conn_id in cooldowns:
            del cooldowns[conn_id]
        if conn_id in scan_timers:
            del scan_timers[conn_id]