from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn

app = FastAPI(title="Server 1: API Gateway")

# Enable CORS for the mobile app and dashboard
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
    Accepts an image and instantly forwards it to Server 2 for the full ML pipeline.
    """
    async with httpx.AsyncClient() as client:
        try:
            # Read file and prepare for forwarding
            file_bytes = await file.read()
            files = {'file': (file.filename, file_bytes, file.content_type)}
            
            # Forward to Server 2
            response = await client.post(f"{SERVER2_URL}/internal/full-pipeline", files=files, timeout=60.0)
            response.raise_for_status()
            
            # Return final audio/text payload to client
            return response.json()
            
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Server 2 is unavailable: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Error from Server 2: {e.response.text}")

@app.post("/api/gesture")
async def process_gesture(payload: dict):
    """
    Simulates processing a sequence of gesture frames to return a command.
    """
    frames = payload.get("frames", [])
    if not frames:
        raise HTTPException(status_code=400, detail="No frames provided in payload")
    
    def process_bilstm_gesture(frames_data):
        # Placeholder function to mock BiLSTM execution
        print(f"[ML MOCK] Processing {len(frames_data)} gesture frames...")
        if len(frames_data) > 20:
            return "SOS"
        elif len(frames_data) > 10:
            return "REPEAT"
        else:
            return "CAPTURE"
    
    command = process_bilstm_gesture(frames)
    return {"status": "success", "command": command}

@app.post("/api/sos")
async def trigger_sos(payload: dict):
    """
    Mocks triggering an emergency SOS alert.
    """
    location = payload.get("location", "Unknown Location")
    # Mocking database / alert system
    print(f"\n🚨 [URGENT] SOS ALERT TRIGGERED 🚨")
    print(f"📍 Location: {location}\n")
    return {"status": "success", "message": "Emergency alert triggered successfully"}

@app.post("/api/report-hazard")
async def report_hazard(payload: dict):
    """
    Mocks saving a crowd-sourced hazard report to a database.
    """
    location = payload.get("location", "Unknown Location")
    hazard_type = payload.get("hazard_type", "Unknown Hazard")
    
    # Mock database save
    print(f"[DB MOCK] Saved hazard '{hazard_type}' at location: {location}")
    return {"status": "success", "message": "Hazard reported successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
