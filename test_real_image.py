import requests
import json
import os

# ==========================================
# 🔧 CONFIGURATION
# Update this string to the absolute path of your real image!
# Example: "C:/Users/yashy/Downloads/test_scene.jpg"
IMAGE_PATH = "test-Image2.png" 

# We test the full flow by hitting Server 1 (Gateway)
# Server 1 will automatically forward it to Server 2 (192.168.0.44)
SERVER1_URL = "http://localhost:8000/api/analyze"
# ==========================================

# Terminal Colors
GREEN = '\033[92m'
BLUE = '\033[94m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def test_real_image():
    print(f"{BLUE}===================================================={RESET}")
    print(f"{BLUE}👁️ OmniVision Real Image ML Test{RESET}")
    print(f"{BLUE}====================================================\n{RESET}")

    if not os.path.exists(IMAGE_PATH):
        print(f"{RED}❌ Error: Could not find image at '{IMAGE_PATH}'{RESET}")
        print(f"{YELLOW}Please open 'test_real_image.py' and update the IMAGE_PATH variable to point to a real image on your computer.{RESET}")
        return

    print(f"🚀 Sending {YELLOW}'{os.path.basename(IMAGE_PATH)}'{RESET} to Server 1...")
    
    try:
        with open(IMAGE_PATH, 'rb') as img_file:
            # We package it exactly as the mobile app would
            files = {'file': (os.path.basename(IMAGE_PATH), img_file, 'image/jpeg')}
            
            print(f"⏳ Waiting for Server 2 (192.168.0.44) to analyze the scene... (This may take up to 60s)")
            response = requests.post(SERVER1_URL, files=files, timeout=60.0)
            
        status_code = response.status_code
        
        if status_code == 200:
            data = response.json()
            print(f"\n{GREEN}✅ Success!{RESET}\n")
            
            # Print the text description nicely
            if "data" in data and "text" in data["data"]:
                ai_text = data['data']['text']
                print(f"{BLUE}🤖 AI Scene Description:{RESET}")
                print("-" * 50)
                print(f"{GREEN}{ai_text}{RESET}")
                print("-" * 50)
            else:
                print(f"{YELLOW}⚠️ Unexpected response format:{RESET}")
                print(json.dumps(data, indent=2))
                
        elif status_code == 503:
            print(f"\n{RED}❌ Server 2 (192.168.0.44) is offline or unreachable from Server 1.{RESET}")
            print(response.text)
        else:
            print(f"\n{RED}❌ Error {status_code}{RESET}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print(f"\n{RED}❌ Connection Error: Could not connect to {SERVER1_URL}. Is Server 1 running?{RESET}")
    except Exception as e:
        print(f"\n{RED}❌ Unexpected Error: {str(e)}{RESET}")

if __name__ == "__main__":
    test_real_image()
