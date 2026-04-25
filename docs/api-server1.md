# Server 1 API Reference

This document outlines the REST API endpoints available on Server 1 (API Gateway & Logic). Server 1 runs on port `8000` and serves as the primary backend gateway for the mobile app.

## Core Endpoints

### 1. Analyze Image
* **Endpoint:** `POST /api/analyze`
* **Content-Type:** `multipart/form-data`
* **Description:** Accepts an image from the client and forwards it to Server 2's full ML pipeline (YOLOv8 -> LLaVA -> Local TTS). Once Server 2 finishes processing, Server 1 returns the final text and audio payload to the client.
* **Request Body:**
  * `file`: (UploadFile) The image to be analyzed.
* **Response (Success - 200 OK):**
  ```json
  {
    "description": "The scene contains a car, traffic light, pedestrian...",
    "audio_base64": "<base64_encoded_audio_string>",
    "detected_objects": ["car", "traffic light", "pedestrian"]
  }
  ```
* **Response (Error - 503):**
  ```json
  {
    "detail": "Server 2 is unavailable: [error message]"
  }
  ```

### 2. Process Gesture
* **Endpoint:** `POST /api/gesture`
* **Content-Type:** `application/json`
* **Description:** Accepts a sequence of hand gesture frames. Evaluates the sequence to map it to a specific command.
* **Request Body:**
  ```json
  {
    "frames": [ "<frame_data_1>", "<frame_data_2>", "..." ] 
  }
  ```
* **Response (Success - 200 OK):**
  ```json
  {
    "status": "success",
    "command": "CAPTURE" // Output could be "CAPTURE", "SOS", or "REPEAT"
  }
  ```

### 3. Emergency SOS
* **Endpoint:** `POST /api/sos`
* **Content-Type:** `application/json`
* **Description:** Triggers an emergency alert using the user's location.
* **Request Body:**
  ```json
  {
    "location": "Latitude, Longitude or Address"
  }
  ```
* **Response (Success - 200 OK):**
  ```json
  {
    "status": "success",
    "message": "Emergency alert triggered successfully"
  }
  ```

### 4. Report Hazard
* **Endpoint:** `POST /api/report-hazard`
* **Content-Type:** `application/json`
* **Description:** Submits a new crowd-sourced hazard report to the database.
* **Request Body:**
  ```json
  {
    "location": "Latitude, Longitude",
    "hazard_type": "pothole, blocked sidewalk, etc."
  }
  ```
* **Response (Success - 200 OK):**
  ```json
  {
    "status": "success",
    "message": "Hazard reported successfully"
  }
  ```

> **Note:** Additional endpoints listed in the architecture documentation (`/api/map-data`, `/api/auth/login`, `/api/auth/register`, and `/api/history`) are reserved for future implementation. All interactions with Server 2 (`/internal/*`) are strictly handled by Server 1 and are not exposed to the mobile app.
