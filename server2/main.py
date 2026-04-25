from fastapi import FastAPI, UploadFile, File, HTTPException
from ultralytics import YOLO
from PIL import Image
import io
import base64
import requests

app = FastAPI(title="Server 2 - Heavy Compute AI Pipeline")

# 1. Load YOLOv8 Model (using the nano version for speed, upgrade to 'yolov8s.pt' if needed)
print("Loading YOLOv8 model...")
yolo_model = YOLO("yolov8n.pt") 

# Ollama local endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

@app.post("/internal/detect")
async def run_yolo(file: UploadFile = File(...)):
    """Runs YOLOv8 only and returns bounding boxes/labels."""
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Run inference
        results = yolo_model(image)
        
        detected_objects = []
        for r in results:
            for box in r.boxes:
                detected_objects.append({
                    "label": yolo_model.names[int(box.cls)],
                    "confidence": float(box.conf)
                })
                
        return {"status": "success", "detections": detected_objects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/internal/describe")
async def run_llava(file: UploadFile = File(...)):
    """Runs LLaVA 1.6 only and returns a text description."""
    try:
        image_bytes = await file.read()
        # Convert image to Base64 for Ollama API
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        payload = {
            "model": "llava:7b-v1.6",
            "prompt": "Describe this image briefly for a visually impaired person. Focus on potential hazards or obstacles.",
            "images": [base64_image],
            "stream": False
        }
        
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        
        description = response.json().get("response", "No description generated.")
        return {"status": "success", "description": description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/internal/full-pipeline")
async def full_pipeline(file: UploadFile = File(...)):
    """Chains YOLOv8, LLaVA, and TTS sequentially."""
    image_bytes = await file.read()
    
    # 1. Run YOLOv8
    image_pil = Image.open(io.BytesIO(image_bytes))
    yolo_results = yolo_model(image_pil)
    hazards = [yolo_model.names[int(box.cls)] for r in yolo_results for box in r.boxes]
    
    # 2. Run LLaVA with context from YOLO
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    context_prompt = f"The following objects were detected: {', '.join(set(hazards))}. Describe the scene for a visually impaired user, prioritizing these immediate hazards."
    
    llava_payload = {
        "model": "llava:7b-v1.6",
        "prompt": context_prompt,
        "images": [base64_image],
        "stream": False
    }
    
    llava_response = requests.post(OLLAMA_API_URL, json=llava_payload).json()
    final_text = llava_response.get("response", "")
    
    # 3. Local TTS (Placeholder for Piper/Coqui integration)
    # audio_path = generate_tts(final_text)
    
    return {
        "status": "success",
        "detections": hazards,
        "text_description": final_text,
        "audio_url": "/path/to/generated/audio.wav" # Replace with actual TTS output
    }