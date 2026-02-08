#!/bin/bash
# Deployment script for AI Todo Agentic System

set -e  # Exit on any error

echo "AI Todo Agentic System - Deployment Script"

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    echo "Error: This script must be run from the project root directory."
    exit 1
fi

echo "
===============================================
Deployment Options:
1. Deploy frontend to Vercel (requires Vercel CLI)
2. Prepare backend for deployment to cloud platform
3. Show deployment guide
===============================================
"

read -p "Select an option (1-3): " option

case $option in
    1)
        echo "
        Deploying frontend to Vercel...
        
        Prerequisites:
        - Vercel CLI installed (npm install -g vercel)
        - Logged in to Vercel (vercel login)
        "
        
        read -p "Continue? (y/n): " confirm
        if [[ $confirm == "y" || $confirm == "Y" ]]; then
            cd frontend
            echo "Installing frontend dependencies..."
            npm install
            echo "Deploying to Vercel..."
            vercel --prod
        fi
        ;;
    2)
        echo "
        Preparing backend for deployment...
        
        This will create a requirements.txt file in the backend directory
        and provide instructions for deployment.
        "
        
        # Copy root requirements.txt to backend if it doesn't exist
        if [ ! -f "backend/requirements.txt" ]; then
            cp requirements.txt backend/requirements.txt
            echo "Copied requirements.txt to backend directory"
        fi
        
        echo "
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
        "
        ;;
    3)
        echo "
        See DEPLOYMENT_GUIDE.md for detailed instructions on deploying
        both frontend and backend components.
        "
        if command -v cat &> /dev/null; then
            cat DEPLOYMENT_GUIDE.md
        else
            echo "Opening deployment guide..."
            if command -v open &> /dev/null; then
                open DEPLOYMENT_GUIDE.md
            elif command -v start &> /dev/null; then
                start DEPLOYMENT_GUIDE.md
            fi
        fi
        ;;
    *)
        echo "Invalid option. Exiting."
        exit 1
        ;;
esac

echo "
Deployment script completed.
"