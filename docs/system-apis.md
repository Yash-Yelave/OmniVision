# Multi-Modal Accessible Navigation System - API Documentation

This document outlines the API endpoints for the entire backend system. It details the distinct roles of the API Gateway (Server 1) and the ML Compute Engine (Server 2), specifically highlighting which routes are exposed to the mobile app and which are strictly for internal inter-server communication.

---

## 📱 Mobile App Facing APIs (Server 1)
These endpoints are exposed on **Port 8000**. The React Native mobile app communicates directly with these routes. Server 1 handles incoming requests, runs lightweight logic (like gesture processing), and securely routes heavy processing tasks to Server 2.

### 1. Analyze Environment
* **Endpoint:** `POST /api/analyze`
* **Content-Type:** `multipart/form-data`
* **Description:** The primary endpoint for visual assistance. The mobile app sends an image here. Server 1 forwards this image to Server 2 for processing and returns the final generated description and audio back to the app.
* **Payload:** `file` (Image)
* **Response (200 OK):**
  ```json
  {
    "text": "There is a park bench three meters ahead.",
    "audio_base64": "<base64_encoded_audio_string>"
  }
  ```

### 2. Process Hand Gesture
* **Endpoint:** `POST /api/gesture`
* **Content-Type:** `application/json`
* **Description:** Evaluates a sequence of hand tracking frames (simulating a BiLSTM model) and determines the user's intended action command.
* **Payload:**
  ```json
  {
    "frames": [ "frame_1_data", "frame_2_data", "..." ]
  }
  ```
* **Response (200 OK):**
  ```json
  {
    "action": "TRIGGER_SCAN" 
  }
  ```

### 3. Trigger Emergency (SOS)
* **Endpoint:** `POST /api/sos`
* **Content-Type:** `application/json`
* **Description:** Initiates an emergency alert protocol, notifying contacts with the user's current GPS location.
* **Payload:**
  ```json
  {
    "lat": "37.7749",
    "lng": "-122.4194"
  }
  ```
* **Response (200 OK):**
  ```json
  {
    "status": "success",
    "message": "Emergency contacts notified"
  }
  ```

### 4. Report Accessibility Hazard
* **Endpoint:** `POST /api/report-hazard`
* **Content-Type:** `application/json`
* **Description:** Submits a new hazard to the crowd-sourced database so that other users can be warned of obstacles.
* **Payload:**
  ```json
  {
    "lat": "37.7749",
    "lng": "-122.4194",
    "hazard_type": "Blocked Sidewalk"
  }
  ```
* **Response (200 OK):**
  ```json
  {
    "status": "success"
  }
  ```

---

## ⚙️ Internal ML APIs (Server 2)
These endpoints are exposed on **Port 8001**. **They are strictly internal.** The mobile app NEVER calls these directly. Server 1 acts as a proxy, communicating with Server 2 via these routes to offload heavy GPU and ML tasks.

### 1. Full ML Pipeline (Used by Server 1)
* **Endpoint:** `POST /internal/full-pipeline`
* **Content-Type:** `multipart/form-data`
* **Description:** This is the endpoint called internally by Server 1's `/api/analyze`. It sequentially runs Object Detection (YOLOv8) -> Vision LLM (LLaVA) -> Local Text-to-Speech (Piper/Coqui).
* **Payload:** `file` (Image)
* **Response (200 OK):**
  ```json
  {
    "text": "There is a park bench three meters ahead.",
    "audio_base64": "<base64_encoded_audio_string>"
  }
  ```

### 2. Isolated Object Detection
* **Endpoint:** `POST /internal/detect`
* **Content-Type:** `multipart/form-data`
* **Description:** Runs only the YOLOv8 model for rapid bounding-box detection without LLM analysis.
* **Payload:** `file` (Image)
* **Response (200 OK):**
  ```json
  {
    "detected_objects": ["park bench", "tree"]
  }
  ```

### 3. Isolated Scene Description
* **Endpoint:** `POST /internal/describe`
* **Content-Type:** `multipart/form-data`
* **Description:** Runs only the LLaVA model to generate text.
* **Payload:** `file` (Image)
* **Response (200 OK):**
  ```json
  {
    "text": "There is a park bench three meters ahead."
  }
  ```

### 4. Isolated Text-to-Speech
* **Endpoint:** `POST /internal/tts`
* **Content-Type:** `application/json`
* **Description:** Converts text into audio.
* **Payload:**
  ```json
  {
    "text": "Warning, tree ahead."
  }
  ```
* **Response (200 OK):**
  ```json
  {
    "audio_base64": "<base64_encoded_audio_string>"
  }
  ```
