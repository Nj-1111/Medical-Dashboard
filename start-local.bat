@echo off
REM =====================================================
REM Medical Dashboard - Local Development Setup
REM Runs backend and frontend locally WITHOUT Docker
REM =====================================================

setlocal enabledelayedexpansion

color 0A
cls

echo.
echo ====================================================
echo  MEDICAL DASHBOARD - LOCAL DEVELOPMENT
echo ====================================================
echo.

REM Check Python
echo [*] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found

REM Check Node.js
echo [*] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
for /f %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
echo [OK] Node.js %NODE_VERSION% found

REM Check PostgreSQL
echo [*] Checking PostgreSQL installation...
psql --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] PostgreSQL not found locally. You'll need to:
    echo    1. Install PostgreSQL from https://www.postgresql.org/download/
    echo    2. OR use Docker to run: docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:15-alpine
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
) else (
    echo [OK] PostgreSQL found
)

REM Create virtualenv if not exists
echo.
echo [*] Setting up Python virtual environment...
if not exist backend\venv (
    cd backend
    python -m venv venv
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment created
) else (
    cd backend
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
)

REM Install Python dependencies
echo [*] Installing Python dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies!
    pause
    exit /b 1
)
echo [OK] Python dependencies installed

REM Setup .env if not exists
if not exist .env (
    echo [*] Creating .env configuration...
    copy .env.example .env
    echo [OK] .env created from template (please update with your settings)
)

REM Run database initialization
echo.
echo [*] Initializing database...
python init_db.py
if errorlevel 1 (
    echo [WARNING] Database initialization failed
    echo Make sure PostgreSQL is running!
    set /p ignore="Continue anyway? (y/n): "
    if /i not "%ignore%"=="y" exit /b 1
)

REM Start backend in new window
echo [*] Starting backend server...
start "Medical Dashboard - Backend" python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

REM Go back to root
cd ..

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Install frontend dependencies
echo [*] Installing frontend dependencies...
cd frontend
if not exist node_modules (
    npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install frontend dependencies!
        pause
        exit /b 1
    )
) else (
    echo [OK] Frontend dependencies already installed
)

REM Start frontend
echo [*] Starting frontend development server...
start "Medical Dashboard - Frontend" npm start

echo.
echo ====================================================
echo [OK] APPLICATIONS STARTING
echo ====================================================
echo.
echo Backend will start at:   http://localhost:8000
echo Frontend will start at:  http://localhost:3000
echo API Docs will be at:     http://localhost:8000/docs
echo.
echo A browser should open automatically to the frontend.
echo.
echo Press Enter to show logs
echo.
pause

cd ..

echo.
echo === BACKEND LOGS ===
echo.

endlocal
