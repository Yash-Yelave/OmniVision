import os
import requests
import json

# Terminal color codes for formatting
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

BASE_URL = "http://localhost:8000"
DUMMY_IMAGE_PATH = "dummy_test_image.jpg"

def create_dummy_image():
    """Creates a small dummy image file for testing."""
    with open(DUMMY_IMAGE_PATH, 'wb') as f:
        # Just write some arbitrary bytes to simulate a binary file
        f.write(os.urandom(1024))
    print(f"{BLUE}[INFO]{RESET} Created dummy image: {DUMMY_IMAGE_PATH}")

def cleanup_dummy_image():
    """Deletes the dummy image file after tests are done."""
    if os.path.exists(DUMMY_IMAGE_PATH):
        os.remove(DUMMY_IMAGE_PATH)
        print(f"{BLUE}[INFO]{RESET} Cleaned up dummy image: {DUMMY_IMAGE_PATH}")

def print_result(endpoint, status_code, response_json):
    """Helper function to print formatted results."""
    # 200 OK -> Green, 503 Unavailable -> Yellow (Expected if Server 2 is down), Others -> Red
    color = GREEN if status_code == 200 else (YELLOW if status_code == 503 else RED)
    print(f"{color}--- Result: {endpoint} ---{RESET}")
    print(f"{color}Status Code: {status_code}{RESET}")
    print(f"Response JSON: \n{json.dumps(response_json, indent=2)}\n")

def test_analyze():
    endpoint = "/api/analyze"
    print(f"{BLUE}[TESTING]{RESET} POST {endpoint}...")
    try:
        with open(DUMMY_IMAGE_PATH, 'rb') as img_file:
            files = {'file': (DUMMY_IMAGE_PATH, img_file, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}{endpoint}", files=files, timeout=70.0)
            
        try:
            resp_json = response.json()
        except Exception:
            resp_json = {"raw_text": response.text}
            
        print_result(endpoint, response.status_code, resp_json)
    except requests.exceptions.ConnectionError:
        print(f"{RED}[ERROR] Could not connect to {BASE_URL}. Is Server 1 running?{RESET}\n")

def test_gesture():
    endpoint = "/api/gesture"
    print(f"{BLUE}[TESTING]{RESET} POST {endpoint}...")
    
    # Create an array of 30 dummy frames (e.g., pairs of coordinates)
    dummy_frames = [[i, i] for i in range(30)]
    payload = {"frames": dummy_frames}
    
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=payload, timeout=10.0)
        print_result(endpoint, response.status_code, response.json())
    except requests.exceptions.ConnectionError:
        print(f"{RED}[ERROR] Could not connect to Server 1.{RESET}\n")

def test_sos():
    endpoint = "/api/sos"
    print(f"{BLUE}[TESTING]{RESET} POST {endpoint}...")
    
    payload = {"lat": 18.5204, "lng": 73.8567}
    
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=payload, timeout=10.0)
        print_result(endpoint, response.status_code, response.json())
    except requests.exceptions.ConnectionError:
        print(f"{RED}[ERROR] Could not connect to Server 1.{RESET}\n")

def test_report_hazard():
    endpoint = "/api/report-hazard"
    print(f"{BLUE}[TESTING]{RESET} POST {endpoint}...")
    
    payload = {
        "lat": 18.5204, 
        "lng": 73.8567, 
        "hazard_type": "Construction"
    }
    
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=payload)
        print_result(endpoint, response.status_code, response.json())
    except requests.exceptions.ConnectionError:
        print(f"{RED}[ERROR] Could not connect to Server 1.{RESET}\n")

if __name__ == "__main__":
    print(f"{BLUE}Starting Server 1 API Tests...{RESET}\n")
    create_dummy_image()
    print("-" * 40)
    
    # Run all tests sequentially
    test_analyze()
    test_gesture()
    test_sos()
    test_report_hazard()
    
    print("-" * 40)
    cleanup_dummy_image()
    print(f"{BLUE}Tests Complete.{RESET}")
