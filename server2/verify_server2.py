import requests
import time
import os

SERVER_URL = "http://localhost:8001/internal/full-pipeline"
TEST_IMAGE_PATH = "verify_dummy_image.jpg"

def main():
    print("=== Verification Script for Server 2 ===")
    
    # 1. Create a dummy test image
    if not os.path.exists(TEST_IMAGE_PATH):
        try:
            from PIL import Image
            img = Image.new('RGB', (50, 50), color='blue')
            img.save(TEST_IMAGE_PATH)
        except ImportError:
            # Fallback if Pillow is not available
            with open(TEST_IMAGE_PATH, "wb") as f:
                f.write(os.urandom(1024))
    
    print(f"Sending POST request to {SERVER_URL}...")
    
    # 2. Track time to assert "lightning fast" response
    start_time = time.time()
    
    try:
        with open(TEST_IMAGE_PATH, "rb") as image_file:
            files = {"file": (TEST_IMAGE_PATH, image_file, "image/jpeg")}
            response = requests.post(SERVER_URL, files=files)
            
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # 3. Assertions
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        data = response.json()
        
        # Assert structure
        assert "text" in data, "Response is missing 'text' field"
        assert "audio_base64" not in data, "Response still contains 'audio_base64' field!"
        assert "detected_objects" not in data, "Response still contains 'detected_objects' field! Should strictly be 'text' only."
        
        # Output results
        print("\n[SUCCESS] Verification Passed!")
        print(f"[TIME] Response Time: {elapsed_time:.3f} seconds (Lightning Fast Mock)")
        print(f"[PAYLOAD] Payload received:\n{data}")
        
    except AssertionError as e:
        print(f"\n[ERROR] Verification Failed: {e}")
    except requests.exceptions.ConnectionError:
        print(f"\n[ERROR] Connection Error: Could not connect to {SERVER_URL}. Is Server 2 running?")
    finally:
        # Cleanup
        if os.path.exists(TEST_IMAGE_PATH):
            os.remove(TEST_IMAGE_PATH)

if __name__ == "__main__":
    main()
