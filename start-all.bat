@echo off
echo Starting GrowthPath Application...
echo.

REM Start backend in new window
echo Starting backend server...
start "GrowthPath Backend" cmd /k "cd backend && start.bat"

REM Wait a moment for backend to start
timeout /t 5 /nobreak > nul

REM Start frontend in new window
echo Starting frontend server...
start "GrowthPath Frontend" cmd /k "cd frontend && start.bat"

echo.
echo GrowthPath is starting!
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop the servers.
pause
