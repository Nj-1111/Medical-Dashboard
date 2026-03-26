@echo off
REM =====================================================
REM Medical Dashboard - Stop Script (Windows)
REM =====================================================

setlocal enabledelayedexpansion

color 0A
cls

echo.
echo ====================================================
echo  MEDICAL DASHBOARD - SHUTDOWN
echo ====================================================
echo.

REM Check docker-compose command
docker-compose --version >nul 2>&1
if errorlevel 1 (
    set COMPOSE_CMD=docker compose
) else (
    set COMPOSE_CMD=docker-compose
)

REM Stop containers
echo [*] Stopping containers...
%COMPOSE_CMD% down --remove-orphans

if errorlevel 1 (
    echo [ERROR] Failed to stop services
    pause
    exit /b 1
)

echo.
echo ====================================================
echo [OK] All services stopped successfully!
echo ====================================================
echo.

REM Optional: Remove volumes
setlocal disabledelayedexpansion
echo.
set /p remove_data="Remove data volumes? (y/n): "
if /i "%remove_data%"=="y" (
    echo [*] Removing volumes...
    %COMPOSE_CMD% down -v
    echo [OK] Volumes removed
)

endlocal
pause
