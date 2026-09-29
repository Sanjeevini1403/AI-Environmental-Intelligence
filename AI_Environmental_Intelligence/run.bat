@echo off
title AI Environmental Intelligence & Smart Mobility System
color 0A

echo ======================================================================
echo    AI-Powered Environmental Intelligence System
echo    Air Quality Prediction & Smart Mobility Recommendations
echo ======================================================================
echo.

:: Check for python or venv
if exist "venv\Scripts\python.exe" (
    set PYTHON_CMD=venv\Scripts\python.exe
) else (
    set PYTHON_CMD=python
)

echo [1/3] Checking environment and dependencies...
%PYTHON_CMD% -c "import fastapi, uvicorn, sklearn, pandas, joblib; print('Dependencies verified.')"
if errorlevel 1 (
    echo [!] Installing required libraries...
    pip install fastapi uvicorn pandas joblib scikit-learn requests
)

echo.
echo [2/3] Launching FastAPI Environmental Backend Server...
echo Server running at: http://127.0.0.1:8000
echo API Documentation: http://127.0.0.1:8000/docs
echo.

:: Automatically open browser after 2 seconds in background
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:8000"

echo [3/3] Starting web server on port 8000 (Press Ctrl+C to stop)...
echo.
%PYTHON_CMD% -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload

pause
