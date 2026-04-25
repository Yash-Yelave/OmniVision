from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn

app = FastAPI(title="Server 1: API Gateway & Gesture Engine")

# Enable CORS for the mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVER2_URL = "http://localhost:8001"

@app.post("/api/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Accepts an image and asynchronously forwards it to Server 2's full-pipeline.
    Returns the exact JSON payload (text and audio_base64) back to the client.
    """
    async with httpx.AsyncClient() as client:
        try:
            file_bytes = await file.read()
            files = {'file': (file.filename, file_bytes, file.content_type)}
            
            response = await client.post(f"{SERVER2_URL}/internal/full-pipeline", files=files, timeout=60.0)
            response.raise_for_status()
            
            return response.json()
            
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Server 2 is unavailable: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Error from Server 2: {e.response.text}")

@app.post("/api/gesture")
async def process_gesture(payload: dict):
    """
    Accepts a JSON payload containing an array representing frames of tracking data.
    """
    frames = payload.get("frames", [])
    if not frames:
        raise HTTPException(status_code=400, detail="No frames provided in payload")
    
    def process_bilstm_gesture(frames_data):
        print(f"[ML MOCK] Processing {len(frames_data)} gesture frames with BiLSTM model...")
        if len(frames_data) > 20:
            return "TRIGGER_SOS"
        elif len(frames_data) > 10:
            return "REPEAT"
        else:
            return "TRIGGER_SCAN"
            
    action = process_bilstm_gesture(frames)
    return {"action": action}

@app.post("/api/sos")
async def trigger_sos(payload: dict):
    """
    Accepts JSON with user location (lat, lng) and triggers emergency alert.
    """
    lat = payload.get("lat", "Unknown")
    lng = payload.get("lng", "Unknown")
    
    print(f"\n🚨 [URGENT] SOS ALERT TRIGGERED 🚨")
    print(f"📍 Location: lat={lat}, lng={lng}\n")
    return {"status": "success", "message": "Emergency contacts notified"}

@app.post("/api/report-hazard")
async def report_hazard(payload: dict):
    """
    Accepts JSON with lat, lng, and hazard_type.
    """
    lat = payload.get("lat", "Unknown")
    lng = payload.get("lng", "Unknown")
    hazard_type = payload.get("hazard_type", "Unknown Hazard")
    
    print(f"[DB MOCK] Saved hazard '{hazard_type}' at location: lat={lat}, lng={lng}")
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
