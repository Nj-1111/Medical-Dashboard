@echo off
REM =====================================================
REM Medical Dashboard - Startup Script (Windows)
REM =====================================================

setlocal enabledelayedexpansion

REM Colors for output
color 0A
cls

echo.
echo ====================================================
echo  MEDICAL DASHBOARD - STARTUP
echo ====================================================
echo.

REM Check if Docker Desktop is running
echo [*] Checking Docker Desktop...
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Desktop is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo [OK] Docker Desktop is running

REM Check if docker-compose is available
echo [*] Checking Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] docker-compose not found. Trying docker compose...
    docker compose version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Docker Compose is not installed!
        pause
        exit /b 1
    )
    set COMPOSE_CMD=docker compose
) else (
    set COMPOSE_CMD=docker-compose
)
echo [OK] Docker Compose is available

REM Load environment variables
if exist .env (
    echo [*] Loading .env configuration...
    for /f "delims== tokens=1,*" %%A in (.env) do (
        if not "%%A"=="" (
            if not "%%A:~0,1%%" == "#" (
                set %%A=%%B
            )
        )
    )
    echo [OK] Environment loaded
) else (
    echo [WARNING] No .env file found. Creating from template...
    if exist backend\.env.example (
        copy backend\.env.example .env
        echo [OK] Created .env from template
    ) else (
        echo [ERROR] .env.example not found!
        pause
        exit /b 1
    )
)

REM Stop any existing containers
echo.
echo [*] Cleaning up existing containers...
%COMPOSE_CMD% down --remove-orphans 2>nul
echo [OK] Cleanup complete

REM Build images
echo.
echo [*] Building Docker images...
%COMPOSE_CMD% build --no-cache
if errorlevel 1 (
    echo [ERROR] Docker build failed!
    pause
    exit /b 1
)
echo [OK] Docker build complete

REM Start services
echo.
echo [*] Starting services...
%COMPOSE_CMD% up -d
if errorlevel 1 (
    echo [ERROR] Failed to start services!
    echo.
    echo [DEBUG] Checking logs:
    %COMPOSE_CMD% logs
    pause
    exit /b 1
)
echo [OK] Services starting...

REM Wait for services to be ready
echo.
echo [*] Waiting for services to be healthy (this may take 1-2 minutes)...
timeout /t 2 /nobreak

:check_health
%COMPOSE_CMD% ps | findstr "medical_backend.*healthy" >nul 2>&1
if errorlevel 1 (
    echo [.] Services still initializing...
    timeout /t 5 /nobreak
    goto check_health
)

echo [OK] All services are healthy!

REM Display service information
echo.
echo ====================================================
echo  SERVICES READY
echo ====================================================
echo.
echo Frontend:    http://localhost:3000
echo   Dashboard: http://localhost:3000/dashboard
echo   Upload:    http://localhost:3000/diagnosis
echo.
echo Backend API: http://localhost:8000
echo   Health:    http://localhost:8000/api/v1/health
echo   Docs:      http://localhost:8000/docs (Swagger UI)
echo.
echo Database:   localhost:5432 (PostgreSQL)
echo Cache:      localhost:6379 (Redis)
echo.
echo Default Credentials:
echo   Email:    test@hospital.com
echo   Password: testpass123
echo.
echo ====================================================
echo.

REM Open frontend in browser
echo [*] Opening dashboard in browser...
start http://localhost:3000/dashboard

echo.
echo Press Ctrl+C to stop services
echo.

REM Show logs
echo [*] Showing live logs (press Ctrl+C to exit):
echo.
%COMPOSE_CMD% logs -f

endlocal
pause

echo.
echo ✓ All services are starting!
echo.
echo To stop services, run:
echo   docker-compose down
echo.
echo To view logs, run:
echo   docker-compose logs -f backend
echo   docker-compose logs -f frontend
echo.

pause
