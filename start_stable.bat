@echo off
REM Stable startup script for AI Todo Agentic System
REM This script will start both backend and frontend with proper configurations

echo ===============================================
echo Starting AI Todo Agentic System...
echo ===============================================

REM Check if we're in the right directory
if not exist "README.md" (
    echo Error: This script must be run from the project root directory.
    pause
    exit /b 1
)

if not exist "frontend" (
    echo Error: frontend directory not found.
    pause
    exit /b 1
)

if not exist "backend" (
    echo Error: backend directory not found.
    pause
    exit /b 1
)

echo.
echo Setting up environment variables...
set DATABASE_URL=sqlite+aiosqlite:///./todo_app.db

echo.
echo Starting Backend Server on port 8001...
echo.

REM Start the backend server in a separate window
start "AI Todo Backend" cmd /k "cd /d %~dp0backend && python -c ^
""import sys; ^
sys.path.insert(0, '..'); ^
import os; ^
os.chdir('..'); ^
from backend.main import app; ^
import uvicorn; ^
print('Backend server starting on http://127.0.0.1:8001'); ^
print('Using database:', os.environ.get('DATABASE_URL', 'sqlite+aiosqlite:///./todo_app.db')); ^
uvicorn.run(app, host='127.0.0.1', port=8001, reload=False)"""

REM Wait a bit for the backend to start
timeout /t 5 /nobreak >nul

echo.
echo Starting Frontend Server on port 3000...
echo.

REM Start the frontend server in a separate window
start "AI Todo Frontend" cmd /k "cd /d %~dp0frontend && set PORT=3000 && npm start"

echo.
echo ===============================================
echo Applications are now starting:
echo - Backend: http://localhost:8001
echo - Frontend: http://localhost:3000
echo.
echo Two separate windows should appear for each server.
echo The system is configured for local development with SQLite database.
echo ===============================================
echo.
echo Waiting for servers to initialize...
echo Please wait for the servers to fully start before accessing them.
echo This may take 30-60 seconds depending on your system.
echo.
pause