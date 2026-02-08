# Deployment Guide for AI Todo Agentic System

## Deploying to Vercel

This application consists of two main components:
1. Frontend: React application in the `frontend` directory
2. Backend: FastAPI application in the `backend` directory

### Option 1: Frontend on Vercel, Backend elsewhere (Recommended)

#### Step 1: Prepare the frontend for Vercel deployment

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Update the proxy in `package.json` to point to your deployed backend API:
   ```json
   "proxy": "https://your-deployed-backend.com"
   ```

3. Or, if using environment variables in your React app, update `.env.production`:
   ```
   REACT_APP_API_URL=https://your-deployed-backend.com
   ```

4. Create a `vercel.json` file in the `frontend` directory:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "package.json",
         "use": "@vercel/static-build",
         "config": {
           "buildCommand": "npm install && npm run build",
           "outputDirectory": "build"
         }
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "/index.html"
       }
     ]
   }
   ```

#### Step 2: Deploy the frontend to Vercel

1. Install the Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Navigate to the `frontend` directory and deploy:
   ```bash
   cd frontend
   vercel --prod
   ```

#### Step 3: Deploy the backend separately

For the backend, you have several options:
- Deploy to Heroku, Render, Railway, or AWS
- Containerize with Docker and deploy to cloud providers
- Use cloud platforms that support containerized applications

**Important Note**: The backend cannot be deployed as serverless functions on Vercel because:
- It uses persistent database connections with SQLAlchemy async engines
- It requires long-running processes for database operations
- Serverless functions are not suitable for applications with persistent connections

### Option 2: Alternative approach using Vercel Edge Functions (Advanced - Not Recommended)

While Vercel supports Edge Functions, this application's architecture with persistent database connections and async operations is not compatible with serverless functions. Converting it would require significant refactoring of the database layer and application architecture.

### Important Notes:

1. **Environment Variables**: Make sure to set up your environment variables in both platforms:
   - For Vercel: Go to your Vercel dashboard → Project → Settings → Environment Variables
   - For backend platform: Follow the respective platform's environment variable setup
   - Add all necessary variables from your `.env` file

2. **Database**: If using Neon PostgreSQL, make sure your connection string is properly configured in the deployed backend environment.

3. **CORS**: Update CORS settings in your backend to allow requests from your Vercel frontend domain.

4. **API Endpoint**: Update the API endpoint in your frontend to point to your deployed backend URL.

## Sample Production Environment Configuration

### Frontend (.env.production)
```
REACT_APP_API_URL=https://your-backend-domain.com
```

### Backend Environment Variables
```
DATABASE_URL=postgresql+asyncpg://username:password@host:port/database
OPENAI_API_KEY=your_openai_api_key
MCP_SERVER_URL=your_mcp_server_url
JWT_SECRET_KEY=your_jwt_secret
```

## Deployment Steps Summary:

1. Deploy backend to a suitable platform (Heroku, Render, etc.) that supports persistent connections
2. Update frontend to point to deployed backend API
3. Deploy frontend to Vercel
4. Configure environment variables in both platforms
5. Test the integration