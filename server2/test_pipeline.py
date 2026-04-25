import requests
import base64
import os

SERVER_URL = "http://127.0.0.1:8001/internal/full-pipeline"
TEST_IMAGE_PATH = "test_image.jpg"

def main():
    # 1. Create a dummy test image if it doesn't exist
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"Creating a dummy test image at {TEST_IMAGE_PATH}...")
        try:
            from PIL import Image
            img = Image.new('RGB', (100, 100), color='red')
            img.save(TEST_IMAGE_PATH)
        except ImportError:
            print("Pillow not installed. Please add a real image named 'test_image.jpg' to this folder to test.")
            return

    print(f"Sending POST request to {SERVER_URL}...")
    
    # 2. Send the multipart/form-data request
    try:
        with open(TEST_IMAGE_PATH, "rb") as image_file:
            files = {"file": (TEST_IMAGE_PATH, image_file, "image/jpeg")}
            response = requests.post(SERVER_URL, files=files)
            
        if response.status_code == 200:
            print("\n[SUCCESS] Received valid response:")
            data = response.json()
            
            print(f"-> Detected Objects: {data.get('detected_objects')}")
            print(f"-> Description: {data.get('description')}")
            
            # Save the audio file to verify it
            audio_b64 = data.get("audio_base64", "")
            if audio_b64:
                audio_bytes = base64.b64decode(audio_b64)
                with open("output_test_audio.wav", "wb") as f:
                    f.write(audio_bytes)
                print("\n[SUCCESS] Audio successfully decoded and saved to 'output_test_audio.wav'")
            else:
                print("\n[WARNING] No audio received in response.")
                
        else:
            print(f"\n[FAILED] with status code: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print(f"\n[ERROR] Could not connect to Server 2 at {SERVER_URL}. Please ensure uvicorn is running.")

if __name__ == "__main__":
    main()
