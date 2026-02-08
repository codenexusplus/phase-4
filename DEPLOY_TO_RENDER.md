# Deploying Backend to Render

## Prerequisites

1. A GitHub account
2. A Render account (sign up at https://render.com)
3. Your code pushed to a GitHub repository

## Step 1: Push your code to GitHub

If you haven't already, create a GitHub repository and push your code:

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit"

# Create a new repository on GitHub (without README)
# Then link and push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
git branch -M main
git push -u origin main
```

## Step 2: Create a PostgreSQL database on Render

1. Log in to your Render dashboard
2. Click "New +" and select "PostgreSQL"
3. Give your database a name
4. Select the free plan
5. Click "Create Database"
6. Note down the external database URL - you'll need this later

## Step 3: Deploy the backend service

1. Go back to your Render dashboard home
2. Click "New +" and select "Web Service"
3. Connect your GitHub account if prompted
4. Select your repository
5. Select the `main` branch
6. Give your service a name (e.g., `ai-todo-backend`)
7. Select the region closest to your users
8. For the root directory, enter: `backend`
9. For the runtime, select: `Python`
10. For the build command, enter: `pip install -r requirements.txt`
11. For the start command, enter: `uvicorn backend.main:app --host=0.0.0.0 --port=$PORT`
12. Click "Create Web Service"

## Step 4: Set environment variables

After creating the web service, you'll need to add environment variables:

1. Go to your newly created web service in the Render dashboard
2. Click on "Environment" tab
3. Add the following environment variables:

```
DATABASE_URL=your_postgresql_database_url_from_step_2
OPENAI_API_KEY=your_openai_api_key
OLLAMA_API_KEY=your_ollama_api_key_if_using_ollama
OLLAMA_BASE_URL=your_ollama_base_url_if_using_ollama
JWT_SECRET_KEY=a_random_secret_string_for_jwt_tokens
DEBUG=False
```

4. Click "Save Changes"

## Step 5: Wait for deployment

Render will now build and deploy your backend. This may take a few minutes. You can monitor the progress in the "Manual Deploy" section.

## Step 6: Get your backend URL

Once the deployment is complete, you'll see your backend URL in the Render dashboard (something like `https://your-service-name.onrender.com`).

## Step 7: Update your frontend

Now that your backend is deployed:

1. Go to your frontend deployment on Vercel
2. In the Vercel dashboard, go to your frontend project
3. Go to Settings → Environment Variables
4. Update the `REACT_APP_API_URL` variable to your backend URL with `/api` appended
   - Example: `https://your-service-name.onrender.com/api`
5. Redeploy your frontend from the Vercel dashboard

## Step 8: Test your application

Visit your frontend URL to test that everything is working correctly.

## Troubleshooting

If you encounter issues:

1. Check the logs in your Render dashboard for the backend service
2. Make sure all environment variables are correctly set
3. Verify that your database connection string is correct
4. Ensure the CORS settings in your backend allow requests from your frontend domain

## Health Check

You can verify your backend is running by visiting: `https://your-service-name.onrender.com/health`