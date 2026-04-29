# OmniVision: Server 2 (WebSocket Architecture Backup)

This folder contains the rewritten, advanced architecture for Server 2. It upgrades the REST API to a **Real-Time WebSocket Stream** and includes a built-in YOLO Logic Gate and Cooldown Mechanism to prevent unnecessary LLM calls.

## Files Included
- `main.py` - The FastAPI WebSocket Server.
- `test_client.py` - A script that uses your computer's webcam to stream frames to the server, simulating the mobile app.
- `test_ws.py` - A basic headless script to test sending a single image.
- `requirements.txt` - Dependencies needed to run this folder.

---

## 🚀 How to Run the Server & Client

You will need **two separate terminal windows**.

### Terminal 1: Start the Backend Server

1. **Open a terminal** and navigate to this folder:
   ```powershell
   cd D:\OmniVision\server2_new_arch
   ```

2. **Activate the Virtual Environment**:
   (We reuse the environment from the main `server2` folder)
   ```powershell
   ..\server2\.server2_env\Scripts\activate
   ```

3. **Install Dependencies** (if you haven't already):
   ```powershell
   pip install -r requirements.txt
   ```

4. **Start the Server**:
   *(We run this on port 8002 to avoid conflicting with your main Server 2)*
   ```powershell
   uvicorn main:app --host 0.0.0.0 --port 8002
   ```

Keep this terminal open and running.

---

### Terminal 2: Start the Webcam Test Client

1. **Open a second, new terminal window** and navigate to this folder:
   ```powershell
   cd D:\OmniVision\server2_new_arch
   ```

2. **Activate the Virtual Environment**:
   ```powershell
   ..\server2\.server2_env\Scripts\activate
   ```

3. **Run the Client**:
   ```powershell
   python test_client.py
   ```

### What to Expect
- A small video window will pop up showing your webcam feed.
- The `test_client.py` terminal will print a highly visible **`[AI HAZARD ALERT RECEIVED]`** box whenever YOLO detects an object and LLaVA generates a description.
- To stop the stream, click on the video window and press the **`q`** key.
