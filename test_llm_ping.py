import requests
import json

GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

BASE_URL = "http://localhost:8000"

def test_llm_ping():
    endpoint = "/api/test-llm"
    print(f"{BLUE}[TESTING]{RESET} Sending LLM ping to {BASE_URL}{endpoint}...")
    
    payload = {"prompt": "Hello AI, are you receiving me? Reply with a short yes."}
    
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=payload, timeout=70.0)
        
        status_code = response.status_code
        # Color coding: 200 = Green, 503 (Server/Ollama Down) = Yellow, Others = Red
        color = GREEN if status_code == 200 else (YELLOW if status_code == 503 else RED)
        
        print(f"{color}--- Result: {endpoint} ---{RESET}")
        print(f"{color}Status Code: {status_code}{RESET}")
        
        try:
            resp_json = response.json()
            print(f"Response JSON: \n{json.dumps(resp_json, indent=2)}\n")
            if status_code == 200 and "response" in resp_json:
                print(f"{GREEN}[SUCCESS] LLM says: {resp_json['response']}{RESET}")
        except Exception:
            print(f"Raw Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"{RED}[ERROR] Could not connect to {BASE_URL}. Is Server 1 running?{RESET}\n")

if __name__ == "__main__":
    test_llm_ping()
