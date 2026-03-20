@echo off
echo.
echo ========================================
echo RESTARTING FLASK WITH NEW MODEL
echo ========================================
echo.

REM Kill all Python processes
echo Stopping all Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 3 /nobreak

REM Clear browser cache message
echo.
echo IMPORTANT: Clear your browser cache!
echo Press Ctrl+Shift+Delete and clear all data
echo.
pause

REM Start Flask
echo.
echo Starting Flask app...
echo Wait for: "Running on http://localhost:5000"
echo.
python crop-disease-detection/app.py

pause
