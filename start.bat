@echo off
REM WiFi Access Database - Startup Script for Windows

echo ==========================================
echo WiFi Access Database - Startup Script
echo ==========================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Check if .env exists, if not create from template
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please update .env with your configuration
)

REM Initialize database
echo.
echo Initializing database...
python init_db.py

REM Start the application
echo.
echo Starting application...
python main.py

pause
