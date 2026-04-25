# Server 2 API Documentation

This document outlines the active REST API endpoints exposed by Server 2 (The Heavy Compute Engine) in the OmniVision architecture.

## Base URL
When running locally: `http://localhost:8001`  
When accessed by Server 1 over the network: `http://192.168.0.44:8001`

*(Note: The server binds to `0.0.0.0` to allow external local-network traffic).*

---

## 1. Full Image Pipeline (Lightweight Mode)

This endpoint ingests an image, runs object detection (mocked YOLOv8), and generates a contextual scene description using a local Vision LLM (Ollama/LLaVA). It deliberately strips out TTS processing to reduce network latency.

### **Endpoint**
`POST /internal/full-pipeline`

### **Headers**
- **Content-Type**: `multipart/form-data`
- **CORS**: Explicitly allows origins from `http://192.168.0.140:8000` and `*`.

### **Request Body**
The request must be sent as `multipart/form-data` with the following field:
| Field | Type | Description |
| :--- | :--- | :--- |
| `file` | File (Binary) | The raw image file (JPEG/PNG) to be processed. |

### **Response**
The endpoint returns a strict JSON payload. It no longer returns audio base64 data.

**Status Code**: `200 OK`

**Content-Type**: `application/json`

**Body Structure**:
```json
{
  "text": "This is a dummy text description. The scene contains: person, car, stop_sign."
}
```

### **Error Responses**
- **`422 Unprocessable Entity`**: If the `file` field is missing from the multipart payload.
- **`500 Internal Server Error`**: If the local Ollama instance crashes or fails to process the image.

---

## Testing via cURL
You can ping this API directly from your terminal or Server 1 using the following cURL command:

```bash
curl -X POST "http://192.168.0.44:8001/internal/full-pipeline" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/image.jpg"
```
