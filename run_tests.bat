@echo off
title TruthLens AI - Test Suite
echo ====================================================
echo Running TruthLens AI Comprehensive Test Suite
echo ====================================================
cd /d "%~dp0"
backend\.venv\Scripts\pytest.exe backend\tests -v
pause
