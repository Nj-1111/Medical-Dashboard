@echo off
REM Medical Diagnosis Pipeline - Docker Startup Script

echo.
echo =====================================
echo Medical Diagnosis Pipeline
echo Docker Startup Script
echo =====================================
echo.

REM Check if Docker is running
echo Checking Docker status...
docker ps >nul 2>&1

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Docker is not running!
    echo.
    echo Please start Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)

echo ✓ Docker is running

echo.
echo Starting services...
echo.

REM Start Docker Compose
docker-compose up -d

REM Wait a moment for services to start
timeout /t 5 /nobreak

echo.
echo =====================================
echo Services Starting...
echo =====================================
echo.
echo Frontend:  http://localhost:3000
echo API Docs:  http://localhost:8000/docs
echo Health:    http://localhost:8000/api/v1/health
echo.
echo Waiting for services to be ready...
echo.

REM Check services status
docker-compose ps

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
