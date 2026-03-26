@echo off
REM Medical Diagnosis Pipeline - Docker Stop Script

echo.
echo =====================================
echo Stopping Medical Diagnosis Pipeline
echo =====================================
echo.

docker-compose down

echo.
echo ✓ All services stopped!
echo.
pause
