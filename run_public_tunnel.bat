@echo off
title TruthLens AI - Public Internet Tunnel (Cloudflare)
echo ====================================================
echo Starting TruthLens AI Public Tunnel via Cloudflare
echo Local Server: http://127.0.0.1:5173
echo ====================================================
cd /d "%~dp0"
npx --yes cloudflared tunnel --url http://127.0.0.1:5173
pause
