import asyncio
import websockets
import time

async def test_websocket():
    uri = "ws://localhost:8001/internal/stream"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket.")
            
            with open("test_image.jpg", "rb") as f:
                image_bytes = f.read()
            
            print("Sending frame 1...")
            await websocket.send(image_bytes)
            
            try:
                # Wait for response (might take a few seconds due to Ollama)
                response = await asyncio.wait_for(websocket.recv(), timeout=20.0)
                print(f"Received from server: {response}")
            except asyncio.TimeoutError:
                print("No response received (either no hazards, or Ollama took too long).")
            
            print("Sending frame 2 immediately (should hit cooldown)...")
            await websocket.send(image_bytes)
            try:
                response2 = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"Received from server (UNEXPECTED): {response2}")
            except asyncio.TimeoutError:
                print("Frame 2 ignored due to cooldown, as expected.")
                
            print("Waiting 6 seconds for cooldown to clear...")
            await asyncio.sleep(6)
            
            print("Sending frame 3 (should process)...")
            await websocket.send(image_bytes)
            try:
                response3 = await asyncio.wait_for(websocket.recv(), timeout=20.0)
                print(f"Received from server: {response3}")
            except asyncio.TimeoutError:
                print("No response received.")
                
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())
