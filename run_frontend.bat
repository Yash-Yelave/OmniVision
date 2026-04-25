@echo off
echo ====================================================
echo 🚀 Starting OmniVision Frontend...
echo ====================================================

cd server1\frontend

:: Automatically install dependencies if they are missing
if not exist node_modules\ (
    echo [INFO] First time setup: Installing dependencies...
    npm install
)

echo.
echo [INFO] Starting Vite Development Server...
echo [INFO] (Using --host so your mobile phone can connect to it!)
echo.

:: Run Vite and expose it to the local Wi-Fi network
npm run dev -- --host

pause
