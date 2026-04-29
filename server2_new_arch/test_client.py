import cv2
import asyncio
import websockets
import json

async def receiver(websocket):
    """Listens for incoming alerts from the server and prints them beautifully."""
    try:
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            
            # Highly visible terminal alert
            print("\n" + "="*60)
            print(" [AI HAZARD ALERT RECEIVED] ".center(60, " "))
            print("="*60)
            print(f" Detected Objects : {', '.join(data.get('labels', []))}")
            print(f" LLaVA Description: {data.get('llava_text', '')}")
            print("="*60 + "\n")
            
    except websockets.exceptions.ConnectionClosed:
        print("[Receiver] Server disconnected.")
    except Exception as e:
        print(f"[Receiver] Error: {e}")

async def sender(websocket):
    """Captures frames from the webcam and sends them at ~2 FPS."""
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("[Error] Could not open webcam. Make sure another app isn't using it.")
        return
        
    print("[Sender] Webcam opened successfully.")
    print("         Streaming to Server 2 at ~2 FPS. Press 'q' in the video window to quit.\n")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[Sender] Failed to grab frame.")
                break
                
            # Resize frame slightly to make the popup small and manageable
            small_frame = cv2.resize(frame, (640, 480))
            
            # Show visual feedback
            cv2.imshow("OmniVision - Webcam Stream", small_frame)
            
            # cv2.waitKey is necessary to refresh the GUI window. 
            # We use 1ms so it doesn't block the asyncio event loop.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("[Sender] 'q' pressed. Quitting stream...")
                break
                
            # Convert frame to JPEG bytes
            success, encoded_image = cv2.imencode('.jpg', frame)
            if success:
                # Send the bytes over WebSocket
                await websocket.send(encoded_image.tobytes())
                
            # Framerate control: ~2 FPS (wait 0.5 seconds between captures/sends)
            await asyncio.sleep(0.5)
            
    except websockets.exceptions.ConnectionClosed:
        pass # Handled by receiver
    except Exception as e:
        print(f"[Sender] Error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        # Ensure we close the websocket if we break out of the loop
        if not websocket.closed:
            await websocket.close()

async def main():
    uri = "ws://localhost:8002/internal/stream"
    print(f"Attempting to connect to {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("[SUCCESS] Connected to Server 2!\n")
            
            # Run sender and receiver concurrently using bi-directional async loop
            recv_task = asyncio.create_task(receiver(websocket))
            send_task = asyncio.create_task(sender(websocket))
            
            # Wait for either task to finish (sender finishes when 'q' is pressed)
            done, pending = await asyncio.wait(
                [recv_task, send_task], 
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cleanup pending tasks
            for task in pending:
                task.cancel()
                
    except ConnectionRefusedError:
        print("[ERROR] Connection refused. Is Server 2 running on port 8002?")
    except Exception as e:
        print(f"[ERROR] Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
