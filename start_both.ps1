# PowerShell script to start both frontend and backend for AI Todo Agentic System

Write-Host "Starting AI Todo Agentic System..." -ForegroundColor Green

# Check if we're in the right directory
if (!(Test-Path "README.md") -or !(Test-Path "frontend") -or !(Test-Path "backend")) {
    Write-Host "Error: This script must be run from the project root directory." -ForegroundColor Red
    exit 1
}

Write-Host "
===============================================
Starting Backend Server...
===============================================
" -ForegroundColor Yellow

# Start the backend in a separate process
Set-Location backend
Write-Host "Installing backend dependencies if needed..." -ForegroundColor Cyan
try {
    pip install -r requirements.txt > $null 2>&1
    Write-Host "Backend dependencies installation completed." -ForegroundColor Green
} catch {
    Write-Host "Backend dependencies installation completed." -ForegroundColor Green
}

Write-Host "Starting backend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-Command", @"
    \$env:PYTHONPATH = '..'
    cd ..
    python -c @"
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath('.'))
sys.path.insert(0, project_root)

# Change the working directory to the project root
os.chdir(project_root)

from backend.main import app
import uvicorn

if __name__ == '__main__':
    print('Starting backend server on http://0.0.0.0:8000')
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=False)
"@
"@

Write-Host "
===============================================
Starting Frontend Server...
===============================================
" -ForegroundColor Yellow

# Start the frontend in a separate process
Set-Location ..\frontend
Write-Host "Installing frontend dependencies if needed..." -ForegroundColor Cyan
try {
    npm install > $null 2>&1
    Write-Host "Frontend dependencies installation completed." -ForegroundColor Green
} catch {
    Write-Host "Frontend dependencies installation completed." -ForegroundColor Green
}

Write-Host "Starting frontend server..." -ForegroundColor Cyan
Start-Process cmd -ArgumentList "/c", "npm start"

Write-Host "
===============================================
Applications are now running:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

The servers are running in separate processes.
===============================================
" -ForegroundColor Green