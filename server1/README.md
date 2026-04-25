cd server1

python -m venv .server1_env
.server1_env\Scripts\activate

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   3. **Run Server 1**:
   ```bash
   python main.py
   ```
   4. **Run Test Server**:
   ```bash
   python ..\test_llm_ping.py

   ```