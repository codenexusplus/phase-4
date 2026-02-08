@echo off
REM Batch script to start both frontend and backend for AI Todo Agentic System with proper environment handling

echo Starting AI Todo Agentic System...

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

echo ===============================================
echo Starting Backend Server with SQLite...
echo ===============================================

REM Start the backend with SQLite in a separate window
start "Backend Server" cmd /k "cd backend && set DATABASE_URL=sqlite+aiosqlite:///./todo_app.db && python -c "import sys, os; project_root = os.path.dirname(os.path.abspath('.')); sys.path.insert(0, project_root); os.chdir(project_root); from backend.main import app; import uvicorn; print('Starting backend server on http://0.0.0.0:8000'); uvicorn.run(app, host='0.0.0.0', port=8000, reload=False)""

timeout /t 5 /nobreak >nul

echo ===============================================
echo Starting Frontend Server...
echo ===============================================

REM Start the frontend in a separate window
start "Frontend Server" cmd /k "cd frontend && npm install && npm start"

echo ===============================================
echo Applications are now starting:
echo - Backend: http://localhost:8000 (using SQLite database)
echo - Frontend: http://localhost:3000
echo.
echo Two separate windows should appear for each server.
echo Press Ctrl+C in each window to stop the servers.
echo ===============================================

pause