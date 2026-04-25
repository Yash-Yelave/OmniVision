import requests
import sys

# Terminal color codes for a better chat experience
GREEN = '\033[92m'
BLUE = '\033[94m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

BASE_URL = "http://localhost:8000/api/test-llm"

def start_chat():
    print(f"{BLUE}===================================================={RESET}")
    print(f"{BLUE}🚀 Interactive LLM Chat via Server 1 Gateway{RESET}")
    print(f"{BLUE}Type 'exit' or 'quit' to stop chatting.{RESET}")
    print(f"{BLUE}====================================================\n{RESET}")

    while True:
        try:
            # 1. Get input from the user
            user_input = input(f"{GREEN}You:{RESET} ")
            
            # 2. Check for exit commands
            if user_input.strip().lower() in ['exit', 'quit']:
                print(f"\n{BLUE}Exiting chat. Goodbye!{RESET}")
                break
                
            if not user_input.strip():
                continue

            print(f"{YELLOW}Thinking... (Waiting for Server 1 -> 192.168.0.44){RESET}")
            
            # 3. Send payload to Server 1
            payload = {"prompt": user_input}
            response = requests.post(BASE_URL, json=payload, timeout=60.0)
            
            # 4. Handle the response
            if response.status_code == 200:
                data = response.json()
                bot_reply = data.get("response", "No response text found.")
                print(f"\n{BLUE}LLM:{RESET} {bot_reply}\n")
            elif response.status_code == 503:
                print(f"\n{RED}[Error 503] Remote Ollama instance at 192.168.0.44 is unreachable.{RESET}\n")
            else:
                print(f"\n{RED}[Error {response.status_code}] {response.text}{RESET}\n")

        except requests.exceptions.ConnectionError:
            print(f"\n{RED}[ERROR] Could not connect to {BASE_URL}. Is Server 1 running?{RESET}\n")
            break
        except KeyboardInterrupt:
            # Handle CTRL+C gracefully
            print(f"\n\n{BLUE}Exiting chat. Goodbye!{RESET}")
            sys.exit(0)
        except Exception as e:
            print(f"\n{RED}[Unexpected Error] {str(e)}{RESET}\n")

if __name__ == "__main__":
    start_chat()
