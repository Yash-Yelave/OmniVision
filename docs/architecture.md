# Accessible Navigation System — Architecture Specification

## 1. System Overview
The Accessible Navigation System is a real-time assistive technology platform designed for people with visual or mobility impairments. It provides audio cues, hazard detection, and crowd-sourced accessibility data. 

The architecture is built on a microservices model, cleanly separating lightweight business logic and routing from heavy GPU-bound machine learning pipelines.

---

## 2. Client Layer

### **Mobile Application (React Native)**
* **Core Functions:** * Captures single images from the user's environment.
  * Sends sequential REST API requests to Server 1.
  * Plays back generated audio descriptions.
  * Displays text outputs for accessibility.
  * Captures hand gesture frames for interface control.

---

## 3. Server 1 — Main Backend & API Gateway

**Tech Stack:** FastAPI (Python) + ReactJS (PC Dashboard)

Server 1 acts as the primary gateway, handling user management, map services, and routing heavy requests. It ensures the mobile client remains lightweight and secure.

### **Core Components**
* **API Gateway:** Receives and routes all incoming requests from the mobile app.
* **Gesture Recognition:** Processes gesture input using the existing BiLSTM/temporal gesture model.
* **User & Auth Service:** Manages user login, registration, and profiles.
* **Crowd-source DB Handler:** Stores and retrieves user-reported accessibility hazards.
* **Map Service:** Overlays hazard data on OpenStreetMap (using Leaflet.js for the dashboard).
* **Request Forwarder:** Securely forwards environmental images to Server 2 via internal REST API.

### **REST API Endpoints (Exposed to Client)**
* `POST /api/analyze` → Forwards image to Server 2 for full pipeline analysis.
* `POST /api/gesture` → Evaluates gesture frames, returns corresponding action.
* `POST /api/report-hazard` → Saves crowd-sourced hazard report to the database.
* `GET  /api/map-data` → Returns nearby accessibility data points.
* `POST /api/sos` → Triggers an emergency alert.
* `POST /api/auth/login` → Authenticates user.
* `POST /api/auth/register` → Creates new user profile.
* `GET  /api/history` → Retrieves user's previous detections and reports.

---

## 4. Server 2 — Heavy Computation (AI Pipeline)

**Tech Stack:** FastAPI (Internal Only)

Server 2 is dedicated exclusively to resource-intensive machine learning tasks. It is strictly internal and never exposed directly to the public internet or the mobile app.

### **Core Components**
* **Object Detection:** **YOLOv8** for rapid bounding-box detection of immediate hazards.
* **Vision LLM:** **LLaVA 1.6 (via Ollama)** for rich, natural language scene description.
* **Text-to-Speech:** **Local TTS (Piper or Coqui)** for fast, offline, and private audio generation without external dependencies.
* **Full Pipeline Handler:** Chains YOLOv8, LLaVA, and Local TTS sequentially.

### **REST API Endpoints (Exposed to Server 1 Only)**
* `POST /internal/full-pipeline` → Accepts image, returns local TTS audio + descriptive text.
* `POST /internal/detect` → Runs YOLOv8 only (returns bounding boxes/labels).
* `POST /internal/describe` → Runs LLaVA only (returns text).
* `POST /internal/tts` → Runs Local TTS only (returns audio).

---

## 5. Request Flows

### **A. Primary Analysis Flow (Sequential)**
1. **User** captures an image on the mobile phone.
2. **App** sends `POST /api/analyze` to **Server 1**.
3. **Server 1** forwards the request via `POST /internal/full-pipeline` to **Server 2**.
4. **Server 2** executes YOLOv8 to generate a list of detected objects/hazards.
5. **Server 2** passes the image and detected objects to LLaVA, which generates a contextual text description.
6. **Server 2** sends the resulting text to the Local TTS engine (Piper/Coqui) to generate an audio file.
7. **Server 2** returns the bundled audio and text payload back to **Server 1**.
8. **Server 1** routes the response back to the **App**.
9. **App** plays the audio and displays the text for the user.

### **B. Gesture Control Flow**
1. **User** performs a hand gesture using the front camera.
2. **App** sends the gesture frame sequence via `POST /api/gesture` to **Server 1**.
3. **Server 1** processes the sequence using the existing gesture recognition model.
4. **Server 1** returns the intended action (e.g., capture, repeat, SOS, toggle).
5. **App** executes the corresponding action locally.

---

## 6. Database Schema (PostgreSQL on Server 1)

* **`Users`**
  * `id`, `name`, `disability_type`
* **`Hazard_Reports`**
  * `id`, `user_id`, `lat`, `lng`, `hazard_type`, `timestamp`
* **`Detection_History`**
  * `id`, `user_id`, `description`, `audio_path`, `timestamp`
* **`Accessibility_Map`**
  * `id`, `lat`, `lng`, `feature_type`, `verified`

---

## 7. Technology Stack Summary

| Layer | Technology |
| :--- | :--- |
| **Mobile App** | React Native |
| **PC Dashboard** | ReactJS |
| **Server 1 (Gateway)** | FastAPI (Python) |
| **Gesture Model** | Pre-existing temporal gesture model (Hosted on Server 1) |
| **Server 2 (Compute)**| FastAPI (Python) |
| **Object Detection** | YOLOv8 |
| **Vision LLM** | LLaVA 1.6 (via Ollama) |
| **Text to Speech** | Local TTS (Piper / Coqui) |
| **Database** | PostgreSQL |
| **Mapping** | OpenStreetMap + Leaflet.js |
| **Communication** | Sequential REST APIs |