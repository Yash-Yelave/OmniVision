from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn
import base64

app = FastAPI(title="Server 2: ML Compute Engine")

# ==========================================
# Placeholder ML Functions
# ==========================================

def run_yolov8(image_bytes: bytes) -> list:
    print("[ML Pipeline] 1. Running YOLOv8 object detection...")
    return ["park bench", "tree"]

def run_llava(image_bytes: bytes, objects: list) -> str:
    print(f"[ML Pipeline] 2. Running LLaVA (via Ollama) with context objects: {objects}...")
    return "There is a park bench three meters ahead."

def run_local_tts(text: str) -> str:
    print(f"[ML Pipeline] 3. Running Piper/Coqui TTS for text: '{text}'...")
    dummy_wav_data = b"RIFF dummy wav data for " + text.encode('utf-8')
    return base64.b64encode(dummy_wav_data).decode("utf-8")

# ==========================================
# API Routes
# ==========================================

@app.post("/internal/full-pipeline")
async def full_pipeline(file: UploadFile = File(...)):
    """
    Chains YOLOv8 -> LLaVA -> TTS sequentially.
    """
    image_bytes = await file.read()
    
    # Step 1: Detect objects
    objects = run_yolov8(image_bytes)
    
    # Step 2: Get scene description
    description = run_llava(image_bytes, objects)
    
    # Step 3: Convert description to audio
    audio_b64 = run_local_tts(description)
    
    return {
        "text": description,
        "audio_base64": audio_b64
    }

@app.post("/internal/detect")
async def detect_objects(file: UploadFile = File(...)):
    """Runs YOLOv8 only."""
    image_bytes = await file.read()
    objects = run_yolov8(image_bytes)
    return {"detected_objects": objects}

@app.post("/internal/describe")
async def describe_scene(file: UploadFile = File(...)):
    """Runs LLaVA only."""
    image_bytes = await file.read()
    description = run_llava(image_bytes, ["unknown object"])
    return {"text": description}

@app.post("/internal/tts")
async def generate_audio(payload: dict):
    """Runs Local TTS only."""
    text = payload.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
    audio_b64 = run_local_tts(text)
    return {"audio_base64": audio_b64}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)