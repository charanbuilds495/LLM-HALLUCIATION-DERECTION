@echo off
title TruthLens AI - Backend Server
echo ====================================================
echo Starting TruthLens AI - FastAPI Backend Server
echo Model: cross-encoder/nli-deberta-v3-base
echo Backend API: http://127.0.0.1:8000
echo Swagger Docs: http://127.0.0.1:8000/docs
echo ====================================================
cd /d "%~dp0backend"
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
