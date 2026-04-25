import requests
import json
from PIL import Image
import io
import os

SERVER2_URL = "http://192.168.0.44:8001"

def create_red_image():
    """Generates a 100x100 solid red image in memory."""
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr

def test_full_pipeline():
    print(f"🚀 Testing Server 2 pipeline directly at {SERVER2_URL}/internal/full-pipeline...")
    
    img_bytes = create_red_image()
    # Note: Server 2 endpoint expects the form field to be named 'file'
    files = {'file': ('red_image.jpg', img_bytes, 'image/jpeg')}
    
    try:
        print("⏳ Waiting up to 120s for Server 2 (YOLOv8 -> LLaVA) to process...")
        response = requests.post(f"{SERVER2_URL}/internal/full-pipeline", files=files, timeout=120.0)
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Success! Received 200 OK")
            print(f"Response JSON:\n{json.dumps(data, indent=2)}")
            
            if "text" in data:
                print(f"\n📝 Extracted Text: {data['text']}")
            else:
                print("\n⚠️ Warning: No 'text' field found in response.")
        else:
            print(f"\n❌ Error {response.status_code} from Server 2")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Connection Error: Could not connect to {SERVER2_URL}")
        print(f"Details: {str(e)}")

if __name__ == "__main__":
    test_full_pipeline()
