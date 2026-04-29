# Server 1: Gateway & REST APIs

This directory contains the primary backend logic for the OmniVision system.

## Components
1. **`main.py`** (Port 8000): Handles core REST APIs (`/api/analyze`, `/api/chat`, etc.) and routes text/image inference to Server 2 or Ollama.
2. **`gateway.py`** (Port 8002): High-speed, bi-directional WebSocket proxy (`/api/stream`) and the foundational PostgreSQL database models using SQLAlchemy.

## Setup Instructions

1. **Activate Virtual Environment:**
   ```bash
   cd server1
   python -m venv .server1_env
   .server1_env\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

You can run both servers simultaneously in two different terminal windows.

**Terminal 1: Run the standard REST APIs**
```bash
python main.py
# Runs on http://0.0.0.0:8000
```

**Terminal 2: Run the WebSocket Proxy & Database Server**
```bash
python gateway.py
# Runs on http://0.0.0.0:8002
```

## Environment Variables
If your Server 2 (Machine Learning Engine) is hosted on a different machine, you can change its target IP by setting environment variables before running the server:
- `SERVER_2_IP` (Default: `192.168.0.44`)
- `DATABASE_URL` (Default: `postgresql://user:pass@localhost:5432/omnivision`)