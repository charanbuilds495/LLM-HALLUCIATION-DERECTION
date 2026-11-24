@echo off
title TruthLens AI - Full Launcher with Public Tunnel
echo ====================================================
echo Starting TruthLens AI Backend, Frontend, and Public Tunnel
echo ====================================================

:: 1. Start Backend in background
echo Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "TruthLens-Backend" /min cmd.exe /k "cd /d "%~dp0backend" && .venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

:: 2. Wait 3 seconds for backend to initialize
timeout /t 3 /nobreak >nul

:: 3. Start Frontend in background
echo Starting Vite Frontend on http://127.0.0.1:5173 ...
start "TruthLens-Frontend" /min cmd.exe /k "cd /d "%~dp0frontend" && npm.cmd run dev"

:: 4. Wait 2 seconds
timeout /t 2 /nobreak >nul

:: 5. Start Cloudflare Tunnel
echo Starting Public Cloudflare Tunnel ...
del /f /q "%~dp0tunnel.log" 2>nul
start "TruthLens-Public-Tunnel" /min cmd.exe /k "cd /d "%~dp0" && cloudflared.exe tunnel --url http://127.0.0.1:5173 --logfile "%~dp0tunnel.log""

echo.
echo ====================================================
echo Servers started successfully!
echo Waiting for public URL to be generated...
echo ====================================================
timeout /t 6 /nobreak >nul

:: Extract and display public URL from tunnel.log
findstr /i "trycloudflare.com" "%~dp0tunnel.log"
pause
