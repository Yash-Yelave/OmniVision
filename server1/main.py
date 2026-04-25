from fastapi import FastAPI, UploadFile, File, HTTPException, Request
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

SERVER2_URL = "http://192.168.0.44:8001"

@app.post("/api/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Accepts an image and asynchronously forwards it to Server 2's full-pipeline.
    Returns the exact JSON payload with text description. Audio processing is moved to edge.
    """
    async with httpx.AsyncClient() as client:
        try:
            file_bytes = await file.read()
            files = {'file': (file.filename, file_bytes, file.content_type)}
            
            response = await client.post(f"{SERVER2_URL}/internal/full-pipeline", files=files, timeout=60.0)
            response.raise_for_status()
            
            server2_data = response.json()
            
            return {
                "status": "success",
                "data": {
                    "text": server2_data.get("text", "")
                }
            }
            
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

@app.post("/api/test-llm")
async def test_llm_direct(payload: dict):
    prompt = payload.get("prompt", "")
    if not prompt:
        raise HTTPException(status_code=400, detail="No prompt provided")
        
    ollama_url = "http://192.168.0.44:11434/api/generate"
    ollama_payload = {
        "model": "llava:v1.6",
        "prompt": prompt,
        "stream": False
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(ollama_url, json=ollama_payload, timeout=60.0)
            response.raise_for_status()
            llm_response = response.json().get("response", "")
            return {"response": llm_response}
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Ollama is unreachable: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Error from Ollama: {e.response.text}")

@app.post("/api/chat")
async def chat_intent_router(request: Request):
    """
    Intent router that determines if the user wants to scan the environment or just chat.
    Supports both web frontend ('text') and mobile app ('prompt') payloads.
    """
    try:
        payload = await request.json()
    except Exception as e:
        raw_body = await request.body()
        raise HTTPException(status_code=400, detail=f"Failed to parse JSON. Raw body: {raw_body}")
        
    print(f"\n[DEBUG] /api/chat received payload: {payload}\n")
    
    user_text = payload.get("text", "") or payload.get("prompt", "") or payload.get("message", "")
    user_text = str(user_text).strip().lower()
    
    if not user_text:
        raise HTTPException(status_code=400, detail=f"No text, prompt, or message provided. Received keys: {list(payload.keys())}")
        
    vision_keywords = ["scan", "look", "see", "analyze", "front of me", "environment", "what is this", "what's this", "picture"]
    
    is_vision_intent = any(keyword in user_text for keyword in vision_keywords)
    
    if is_vision_intent:
        return {
            "status": "success",
            "action": "TRIGGER_CAMERA",
            "data": {"text": "Scanning the environment now."},
            "response": "Scanning the environment now." # For mobile app compatibility
        }
    else:
        # Normal Chat - Direct to Ollama to bypass Server 2 route dependencies
        ollama_url = "http://192.168.0.44:11434/api/generate"
        prompt_text = (
            "You are OmniVision, a helpful and friendly accessibility assistant for a visually impaired user. "
            "Engage in a brief, conversational response to the user's message. "
            f"User Message: {user_text}"
        )
        ollama_payload = {
            "model": "llava:v1.6",
            "prompt": prompt_text,
            "stream": False,
            "options": {"temperature": 0.7, "top_k": 40}
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(ollama_url, json=ollama_payload, timeout=30.0)
                response.raise_for_status()
                llm_response = response.json().get("response", "")
                
                return {
                    "status": "success",
                    "action": "SPEAK",
                    "data": {"text": llm_response},
                    "response": llm_response # For mobile app compatibility
                }
            except httpx.RequestError as e:
                raise HTTPException(status_code=503, detail=f"Ollama is unavailable: {str(e)}")
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=502, detail=f"Error from Ollama: {e.response.text}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
