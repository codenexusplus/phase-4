#!/bin/bash
# Backend Deployment Script for AI Todo Agentic System

set -e  # Exit on any error

echo "AI Todo Agentic System - Backend Deployment Script"

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    echo "Error: This script must be run from the project root directory."
    exit 1
fi

echo "
===============================================
Backend Deployment Options:
1. Prepare for Render deployment
2. Prepare for Heroku deployment
3. Create Docker image
4. Show backend deployment guide
===============================================
"

read -p "Select an option (1-4): " option

case $option in
    1)
        echo "
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
        "
        ;;
    2)
        echo "
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
        "
        ;;
    3)
        echo "
        Building Docker image for backend...
        "
        
        cd backend
        echo "Building Docker image..."
        docker build -t ai-todo-backend .
        
        echo "
        Docker image built successfully!
        
        To run locally for testing:
        docker run -p 8000:8000 \\
          -e DATABASE_URL=your_database_url \\
          -e OPENAI_API_KEY=your_openai_key \\
          -e OLLAMA_API_KEY=your_ollama_key \\
          -e OLLAMA_BASE_URL=your_ollama_base_url \\
          -e JWT_SECRET_KEY=your_jwt_secret \\
          ai-todo-backend
        "
        ;;
    4)
        echo "
        See BACKEND_DEPLOYMENT_GUIDE.md for detailed instructions on deploying
        the backend to various platforms.
        "
        if command -v cat &> /dev/null; then
            cat BACKEND_DEPLOYMENT_GUIDE.md
        else
            echo "Opening backend deployment guide..."
            if command -v open &> /dev/null; then
                open BACKEND_DEPLOYMENT_GUIDE.md
            elif command -v start &> /dev/null; then
                start BACKEND_DEPLOYMENT_GUIDE.md
            fi
        fi
        ;;
    *)
        echo "Invalid option. Exiting."
        exit 1
        ;;
esac

echo "
Backend deployment preparation completed.
"