@echo off
echo.
echo ========================================
echo Crop Disease Detection - Starting App
echo ========================================
echo.
echo Verifying setup...
python verify_setup.py
if errorlevel 1 (
    echo.
    echo ERROR: Setup verification failed!
    pause
    exit /b 1
)
echo.
echo Starting Flask app...
echo Open your browser to: http://localhost:5000
echo.
python app.py
pause
