@echo off
title Push TruthLens AI to GitHub
cd /d "%~dp0"
echo ====================================================
echo      TRUTHLENS AI - GITHUB DEPLOYMENT HELPER
echo ====================================================
echo Target Repository:
echo https://github.com/charanbuilds495/LLM-Halluciation-Detection.git
echo ====================================================
echo.

:: 1. Check GitHub CLI authentication
echo [1/3] Checking GitHub authentication status...
gh auth status >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ----------------------------------------------------
    echo [ACTION NEEDED] You are not logged into GitHub yet.
    echo We will now open GitHub in your browser to sign in.
    echo ----------------------------------------------------
    echo.
    gh auth login --hostname github.com --git-protocol https --web
    echo.
    echo Configuring git credential helper...
    gh auth setup-git
) else (
    echo [OK] Already authenticated with GitHub.
)

:: 2. Push to GitHub
echo.
echo [2/3] Pushing all files and branches to GitHub...
echo Command: git push -u origin main --force
git push -u origin main --force

if %errorlevel% equ 0 (
    echo.
    echo ====================================================
    echo [SUCCESS] Your repository is now fully live!
    echo.
    echo View your GitHub Repository:
    echo https://github.com/charanbuilds495/LLM-Halluciation-Detection
    echo.
    echo View your Live Deployed Web Application:
    echo https://charanbuilds495.github.io/LLM-Halluciation-Detection/
    echo ====================================================
) else (
    echo.
    echo ====================================================
    echo [NOTE] If git requested a password above, you can:
    echo 1. Generate a Personal Access Token on GitHub:
    echo    https://github.com/settings/tokens (select 'repo' scope)
    echo 2. Paste the token as your password when prompted.
    echo ====================================================
)

echo.
pause
