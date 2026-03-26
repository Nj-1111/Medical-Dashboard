@echo off
REM Medical Dashboard - Diagnostic and Recovery Utility
REM Identifies and fixes common issues

setlocal enabledelayedexpansion

color 0B
cls

echo.
echo ============================================================================
echo  MEDICAL DASHBOARD - DIAGNOSTIC AND RECOVERY UTILITY
echo ============================================================================
echo.

set /p action="Select action (1=Validate Setup, 2=Fix Common Issues, 3=Full Repair, 4=View Logs): "

if "%action%"=="1" goto validate
if "%action%"=="2" goto fix_issues
if "%action%"=="3" goto full_repair
if "%action%"=="4" goto view_logs
goto invalid_choice

:validate
cls
echo.
echo Running validation script...
python validate_setup.py
pause
goto end

:fix_issues
cls
echo.
echo Attempting to fix common issues...
echo.

echo [*] Step 1: Checking Docker status...
docker ps >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker Desktop.
    pause
    goto end
)
echo [OK] Docker is running

echo [*] Step 2: Removing stopped containers...
docker-compose down --remove-orphans 2>nul

echo [*] Step 3: Cleaning up unused images (optional)
set /p cleanup="Remove unused images? (y/n): "
if /i "%cleanup%"=="y" (
    docker image prune -f
    echo [OK] Cleanup completed
)

echo [*] Step 4: Rebuilding images...
docker-compose build --no-cache
if errorlevel 1 (
    echo [ERROR] Build failed
    pause
    goto end
)

echo [*] Step 5: Starting services...
docker-compose up -d
if errorlevel 1 (
    echo [ERROR] Failed to start services
    docker-compose logs
    pause
    goto end
)

timeout /t 5 /nobreak

echo [*] Step 6: Initializing database...
docker-compose exec backend python init_db.py

echo.
echo [OK] Common issues fixed. Services are starting...
echo.
timeout /t 10 /nobreak
docker-compose ps
pause
goto end

:full_repair
cls
echo.
echo WARNING: Full repair will reset all data!
set /p confirm="Continue? (y/n): "
if /i not "%confirm%"=="y" goto end

echo.
echo [*] Step 1: Stopping all services...
docker-compose down

echo [*] Step 2: Removing all volumes (DATA WILL BE LOST)...
docker-compose down -v
echo [OK] Volumes removed

echo [*] Step 3: Removing images...
docker-compose rm -f
echo [OK] Containers removed

echo [*] Step 4: Cleaning volumes and cache...
docker volume prune -f
echo [OK] Cleanup completed

echo [*] Step 5: Rebuilding everything from scratch...
docker-compose build --no-cache
if errorlevel 1 (
    echo [ERROR] Build failed
    pause
    goto end
)

echo [*] Step 6: Starting fresh services...
docker-compose up -d

timeout /t 5 /nobreak

echo [*] Step 7: Initializing new database...
docker-compose exec backend python init_db.py

echo.
echo [OK] Full repair completed. All data has been reset.
echo.
docker-compose ps
pause
goto end

:view_logs
cls
echo.
echo Displaying service logs (press Ctrl+C to exit)...
echo.
timeout /t 2 /nobreak

docker-compose logs -f

goto end

:invalid_choice
echo Invalid choice. Please try again.
pause
goto end

:end
endlocal
exit /b 0
