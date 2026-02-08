# PowerShell Deployment script for AI Todo Agentic System

Write-Host "AI Todo Agentic System - Deployment Script" -ForegroundColor Green

# Check if we're in the right directory
if (!(Test-Path "README.md") -or !(Test-Path "frontend") -or !(Test-Path "backend")) {
    Write-Host "Error: This script must be run from the project root directory." -ForegroundColor Red
    exit 1
}

Write-Host "
===============================================
Deployment Options:
1. Deploy frontend to Vercel (requires Vercel CLI)
2. Prepare backend for deployment to cloud platform
3. Show deployment guide
===============================================
" -ForegroundColor Yellow

$option = Read-Host "Select an option (1-3)"

switch ($option) {
    1 {
        Write-Host "
        Deploying frontend to Vercel...
        
        Prerequisites:
        - Vercel CLI installed (npm install -g vercel)
        - Logged in to Vercel (vercel login)
        " -ForegroundColor Cyan
        
        $confirm = Read-Host "Continue? (y/n)"
        if ($confirm -eq "y" -or $confirm -eq "Y") {
            Set-Location frontend
            Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
            npm install
            Write-Host "Deploying to Vercel..." -ForegroundColor Cyan
            vercel --prod
        }
    }
    2 {
        Write-Host "
        Preparing backend for deployment...
        
        This will create a requirements.txt file in the backend directory
        and provide instructions for deployment.
        " -ForegroundColor Cyan
        
        # Copy root requirements.txt to backend if it doesn't exist
        if (!(Test-Path "backend\requirements.txt")) {
            Copy-Item requirements.txt backend\requirements.txt
            Write-Host "Copied requirements.txt to backend directory" -ForegroundColor Green
        }
        
        Write-Host "
        Backend prepared for deployment.
        
        Deployment options for backend:
        1. Heroku: Use the Procfile method or container deployment
        2. Render: Use the web service template
        3. Railway: Connect your GitHub repo
        4. AWS/Azure/GCP: Container deployment or server deployment
        
        Remember to set environment variables in your deployment platform:
        - DATABASE_URL
        - OPENAI_API_KEY
        - JWT_SECRET_KEY
        - Any other variables from your .env file
        " -ForegroundColor Cyan
    }
    3 {
        Write-Host "
        See DEPLOYMENT_GUIDE.md for detailed instructions on deploying
        both frontend and backend components.
        " -ForegroundColor Cyan
        
        if (Test-Path "DEPLOYMENT_GUIDE.md") {
            Get-Content "DEPLOYMENT_GUIDE.md"
        } else {
            Write-Host "DEPLOYMENT_GUIDE.md not found." -ForegroundColor Red
        }
    }
    default {
        Write-Host "Invalid option. Exiting." -ForegroundColor Red
        exit 1
    }
}

Write-Host "
Deployment script completed.
" -ForegroundColor Green