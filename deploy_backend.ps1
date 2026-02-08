# PowerShell Backend Deployment Script for AI Todo Agentic System

Write-Host "AI Todo Agentic System - Backend Deployment Script" -ForegroundColor Green

# Check if we're in the right directory
if (!(Test-Path "README.md") -or !(Test-Path "frontend") -or !(Test-Path "backend")) {
    Write-Host "Error: This script must be run from the project root directory." -ForegroundColor Red
    exit 1
}

Write-Host "
===============================================
Backend Deployment Options:
1. Prepare for Render deployment
2. Prepare for Heroku deployment
3. Create Docker image
4. Show backend deployment guide
===============================================
" -ForegroundColor Yellow

$option = Read-Host "Select an option (1-4)"

switch ($option) {
    1 {
        Write-Host "
        Preparing for Render deployment...
        
        Files already prepared:
        - backend/requirements.txt
        - backend/Procfile
        - backend/runtime.txt
        - backend/Dockerfile
        
        To deploy to Render:
        1. Push this code to a GitHub repository
        2. Go to https://render.com and create a new Web Service
        3. Connect to your GitHub repository
        4. Set the root directory to '/backend'
        5. Use the provided Procfile for deployment
        6. Set environment variables in Render dashboard
        " -ForegroundColor Cyan
    }
    2 {
        Write-Host "
        Preparing for Heroku deployment...
        
        Files already prepared:
        - backend/requirements.txt
        - backend/Procfile
        - backend/runtime.txt
        
        To deploy to Heroku:
        1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
        2. Login: heroku login
        3. Create app: heroku create your-app-name
        4. Set buildpack: heroku buildpacks:set heroku/python
        5. Deploy: git push heroku main
        6. Set config vars: heroku config:set KEY=VALUE
        " -ForegroundColor Cyan
    }
    3 {
        Write-Host "
        Building Docker image for backend...
        " -ForegroundColor Cyan
        
        Set-Location backend
        Write-Host "Building Docker image..." -ForegroundColor Cyan
        docker build -t ai-todo-backend .
        
        Write-Host "
        Docker image built successfully!
        
        To run locally for testing:
        docker run -p 8000:8000 `
          -e DATABASE_URL=your_database_url `
          -e OPENAI_API_KEY=your_openai_key `
          -e OLLAMA_API_KEY=your_ollama_key `
          -e OLLAMA_BASE_URL=your_ollama_base_url `
          -e JWT_SECRET_KEY=your_jwt_secret `
          ai-todo-backend
        " -ForegroundColor Green
    }
    4 {
        Write-Host "
        See BACKEND_DEPLOYMENT_GUIDE.md for detailed instructions on deploying
        the backend to various platforms.
        " -ForegroundColor Cyan
        
        if (Test-Path "BACKEND_DEPLOYMENT_GUIDE.md") {
            Get-Content "BACKEND_DEPLOYMENT_GUIDE.md"
        } else {
            Write-Host "BACKEND_DEPLOYMENT_GUIDE.md not found." -ForegroundColor Red
        }
    }
    default {
        Write-Host "Invalid option. Exiting." -ForegroundColor Red
        exit 1
    }
}

Write-Host "
Backend deployment preparation completed.
" -ForegroundColor Green