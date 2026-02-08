# Backend Deployment Guide

This guide will help you deploy the backend of the AI Todo Agentic System to various platforms.

## Deploying to Render

### Step 1: Prepare your repository
1. Make sure all your backend files are in a public GitHub repository
2. The backend files are located in the `backend` directory of your project

### Step 2: Create a Render account
1. Go to https://render.com and sign up for an account
2. Connect your GitHub account to Render

### Step 3: Create a new Web Service
1. Click "New +" and select "Web Service"
2. Connect your GitHub repository
3. Select the branch you want to deploy (usually `main` or `master`)
4. Give your service a name (e.g., `ai-todo-backend`)
5. Choose the region closest to your users

### Step 4: Configure the build and deployment
- Environment: Python
- Runtime: Select the latest Python 3.10 or higher
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn backend.main:app --host=0.0.0.0 --port=$PORT`

### Step 5: Set environment variables
Go to your Render dashboard for this service and add the following environment variables:
- `DATABASE_URL`: Your PostgreSQL database URL (Neon or other)
- `OPENAI_API_KEY`: Your OpenAI API key
- `OLLAMA_API_KEY`: Your Ollama API key (if using)
- `OLLAMA_BASE_URL`: Your Ollama base URL (if using)
- `JWT_SECRET_KEY`: A secret key for JWT tokens
- `DEBUG`: True or False

### Step 6: Deploy
Click "Create Web Service" and Render will build and deploy your backend automatically.

## Deploying to Heroku

### Step 1: Prepare your repository
1. Make sure all your backend files are in a public GitHub repository

### Step 2: Create a Heroku account and install CLI
1. Go to https://heroku.com and sign up for an account
2. Install the Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli

### Step 3: Deploy using Heroku CLI
```bash
# Login to Heroku
heroku login

# Create a new app
heroku create your-app-name

# Set the Python runtime
heroku buildpacks:set heroku/python

# Deploy your code
git push heroku main
```

### Step 4: Set environment variables
```bash
heroku config:set DATABASE_URL=your_database_url
heroku config:set OPENAI_API_KEY=your_openai_key
heroku config:set OLLAMA_API_KEY=your_ollama_key
heroku config:set OLLAMA_BASE_URL=your_ollama_base_url
heroku config:set JWT_SECRET_KEY=your_jwt_secret
heroku config:set DEBUG=False
```

## Deploying using Docker

If you prefer to deploy using Docker:

### Step 1: Build the Docker image
```bash
docker build -t ai-todo-backend .
```

### Step 2: Run the Docker container locally for testing
```bash
docker run -p 8000:8000 -e DATABASE_URL=your_database_url -e OPENAI_API_KEY=your_openai_key ai-todo-backend
```

### Step 3: Deploy to cloud platforms that support Docker
You can deploy this Docker image to various cloud platforms like:
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

## Important Notes

1. **Database**: Make sure to set up a PostgreSQL database (Neon, AWS RDS, etc.) and update the `DATABASE_URL` environment variable accordingly.

2. **Environment Variables**: Never commit sensitive information like API keys to your repository. Always use environment variables.

3. **Health Check**: Your backend has a health check endpoint at `/health` that returns the status of your application.

4. **API Endpoints**: Your main API endpoints are under `/api/{user_id}/chat` and other task-related endpoints.

## After Deployment

Once your backend is deployed:
1. Note down the URL of your deployed backend (e.g., `https://your-app.onrender.com`)
2. Update the frontend's `REACT_APP_API_URL` environment variable in Vercel to point to your backend URL with `/api` suffix (e.g., `https://your-app.onrender.com/api`)
3. Redeploy your frontend on Vercel