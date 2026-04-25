import os
import requests
import base64
import ollama
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Server 2: ML Compute Engine (Lightweight)")

# Explicit CORS configuration for Server 1
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.0.140:8000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_yolov8(image_path: str) -> list:
    """Dummy YOLOv8 function returning mocked labels."""
    return ["person", "car", "stop_sign"]

def run_llava(image_path: str, labels: list) -> str:
    objects_str = ", ".join(labels) if labels else "none"
    
    prompt_text = (
        "You are a strict navigational assistant for a visually impaired user. "
        "Provide a concise, direct description in under 3 sentences. "
        "Focus strictly on immediate spatial awareness (e.g., 'straight ahead', 'to your left'). "
        "Prioritize identifying hazards, obstacles, and path clearance. "
        f"Factually integrate the following objects detected in the scene: [{objects_str}]. "
        "Do NOT make up or hallucinate objects that are not there."
    )
    
    # Ping local Ollama instance
    ollama_client = ollama.Client(host='http://localhost:11434')
    response = ollama_client.generate(
        model='llava:v1.6',
        prompt=prompt_text,
        images=[image_path],
        options={'temperature': 0.2, 'top_k': 40}
    )
    return response.get('response', '')

@app.post("/internal/full-pipeline")
async def full_pipeline(file: UploadFile = File(...)):
    """
    Reduced pipeline: YOLOv8 -> Ollama/LLaVA.
    Returns ONLY the text description. TTS is handled by the mobile app.
    """
    temp_image_path = f"temp_{file.filename}"
    
    try:
        # Save image temporarily
        with open(temp_image_path, "wb") as f:
            f.write(await file.read())
            
        # 1. Object Detection (Mocked)
        labels = run_yolov8(temp_image_path)
        
        # 2. Scene Description (Ping Ollama / Mocked)
        description = run_llava(temp_image_path, labels)
        
        # Return strictly JSON with only "text"
        return JSONResponse(content={"text": description})
        
    finally:
        # Cleanup
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

@app.post("/internal/chat")
async def internal_chat(payload: dict):
    """
    Handles pure conversational text without processing an image.
    Pings the local Ollama instance for a conversational response.
    """
    user_text = payload.get("text", "")
    
    prompt_text = (
        "You are OmniVision, a helpful and friendly accessibility assistant for a visually impaired user. "
        "Engage in a brief, conversational response to the user's message. "
        f"User Message: {user_text}"
    )
    
    ollama_client = ollama.Client(host='http://localhost:11434')
    response = ollama_client.generate(
        model='llava:v1.6',
        prompt=prompt_text,
        options={'temperature': 0.7, 'top_k': 40}
    )
    return JSONResponse(content={"text": response.get('response', '')})