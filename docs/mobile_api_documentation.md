# OmniVision Mobile App API Documentation

This document outlines the REST API endpoints exposed by **Server 1 (API Gateway)** for the OmniVision mobile application. 

**Base URL**
Replace `<SERVER1_IP>` with the local IP address of the machine running Server 1 (e.g., `192.168.0.140`).
```
http://<SERVER1_IP>:8000
```

---

## 1. Image Analysis (Scene Description)
Uploads an image captured by the mobile app for heavy ML processing (Object Detection + Vision LLM). TTS is handled on the mobile edge, so this endpoint strictly returns text.

*   **Endpoint:** `POST /api/analyze`
*   **Content-Type:** `multipart/form-data`

### Request Body
| Field | Type | Description |
| :--- | :--- | :--- |
| `file` | `File` | The raw binary image data (JPEG/PNG) to analyze. |

### Success Response (`200 OK`)
```json
{
  "status": "success",
  "data": {
    "text": "A red car is parked next to a stop sign on a sunny day."
  }
}
```

### Error Responses
*   **`503 Service Unavailable`**: The backend ML Compute Engine (Server 2) is offline or unreachable.
*   **`422 Unprocessable Entity`**: The request is missing the required `file` field.

---

## 2. Process Gesture Data
Sends sequential tracking frames to trigger specific application actions (e.g., starting a scan or triggering an SOS).

*   **Endpoint:** `POST /api/gesture`
*   **Content-Type:** `application/json`

### Request Body
```json
{
  "frames": [
    {"x": 10.5, "y": 20.1, "z": 0.5},
    {"x": 11.0, "y": 20.3, "z": 0.6}
  ]
}
```

### Success Response (`200 OK`)
```json
{
  "action": "TRIGGER_SCAN" 
}
```
*(Note: Current mock implementation returns `TRIGGER_SOS` if frames > 20, `REPEAT` if frames > 10, else `TRIGGER_SCAN`).*

---

## 3. Trigger Emergency SOS
Immediately alerts emergency contacts with the user's current GPS location.

*   **Endpoint:** `POST /api/sos`
*   **Content-Type:** `application/json`

### Request Body
```json
{
  "lat": 18.5204,
  "lng": 73.8567
}
```

### Success Response (`200 OK`)
```json
{
  "status": "success",
  "message": "Emergency contacts notified"
}
```

---

## 4. Report Hazard
Saves a specific hazard type and GPS coordinates to the database to alert other visually impaired users in the area.

*   **Endpoint:** `POST /api/report-hazard`
*   **Content-Type:** `application/json`

### Request Body
```json
{
  "lat": 18.5204,
  "lng": 73.8567,
  "hazard_type": "Construction Zone"
}
```

### Success Response (`200 OK`)
```json
{
  "status": "success"
}
```
