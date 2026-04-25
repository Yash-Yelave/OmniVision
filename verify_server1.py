import os
import requests
import json

BASE_URL = "http://localhost:8000"
DUMMY_IMAGE_PATH = "verify_dummy.jpg"

def create_dummy_image():
    with open(DUMMY_IMAGE_PATH, 'wb') as f:
        # Generate arbitrary binary data
        f.write(os.urandom(1024))

def verify_analyze_endpoint():
    endpoint = "/api/analyze"
    print(f"🚀 Verifying Server 1 endpoint: {endpoint}...")
    
    create_dummy_image()
    
    try:
        with open(DUMMY_IMAGE_PATH, 'rb') as img_file:
            files = {'file': (DUMMY_IMAGE_PATH, img_file, 'image/jpeg')}
            print("⏳ Sending request and waiting up to 60s for Server 2 ML response...")
            response = requests.post(f"{BASE_URL}{endpoint}", files=files, timeout=70.0)
            
        status_code = response.status_code
        print(f"Status Code: {status_code}")
        
        if status_code == 200:
            data = response.json()
            print(f"Response JSON:\n{json.dumps(data, indent=2)}\n")
            
            # Assertions to strictly verify schema
            assert "status" in data, "❌ Response missing 'status' key"
            assert data["status"] == "success", "❌ Response 'status' should be 'success'"
            assert "data" in data, "❌ Response missing 'data' object"
            
            payload_data = data["data"]
            assert "text" in payload_data, "❌ 'text' key is missing inside 'data'!"
            assert "audio_base64" not in payload_data, "❌ AUDIO_BASE64 SHOULD NOT BE PRESENT in 'data'!"
            assert "audio_base64" not in data, "❌ AUDIO_BASE64 SHOULD NOT BE PRESENT at root level!"
            
            print("✅ Verification Passed: The response schema perfectly matches the updated requirements (no audio, only text).")
            
        elif status_code == 503:
            print("⚠️ Status 503: Server 2 (192.168.0.44) is offline. We successfully connected to Server 1, but cannot fully verify the payload schema until Server 2 is running.")
            print(f"Detail: {response.text}")
        else:
            print(f"❌ Unexpected status code: {status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: Could not connect to {BASE_URL}. Is Server 1 running?")
    except AssertionError as ae:
        print(f"❌ Assertion Error: {str(ae)}")
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
    finally:
        if os.path.exists(DUMMY_IMAGE_PATH):
            os.remove(DUMMY_IMAGE_PATH)
            print("\n🧹 Cleaned up dummy image.")

if __name__ == "__main__":
    verify_analyze_endpoint()
