#!/bin/bash
# Script to start both frontend and backend for AI Todo Agentic System

set -e  # Exit on any error

echo "Starting AI Todo Agentic System..."

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    echo "Error: This script must be run from the project root directory."
    exit 1
fi

echo "
===============================================
Starting Backend Server...
===============================================
"

# Start the backend in the background
cd backend
echo "Installing backend dependencies if needed..."
pip install -r requirements.txt > /dev/null 2>&1 || echo "Backend dependencies installation completed."

echo "Starting backend server..."
python -c "
import sys
import os
import subprocess

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
" &
BACKEND_PID=$!

echo "Backend started with PID: $BACKEND_PID"

# Wait a moment for the backend to start
sleep 3

echo "
===============================================
Starting Frontend Server...
===============================================
"

# Start the frontend in the background
cd ../frontend
echo "Installing frontend dependencies if needed..."
npm install > /dev/null 2>&1 || echo "Frontend dependencies installation completed."

echo "Starting frontend server..."
npm start &

echo "
===============================================
Applications are now running:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

Press Ctrl+C to stop both servers.
===============================================
"

# Wait for both processes to finish
wait $BACKEND_PID