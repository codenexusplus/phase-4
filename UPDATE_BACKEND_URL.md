# Instructions to update backend URL in Vercel

1. First, make sure you have deployed your backend to a platform like Render, Heroku, etc.
   - Example backend URL: https://my-ai-todo-backend.onrender.com

2. To update the environment variable in Vercel:
   - Go to https://vercel.com/dashboard
   - Select your project (likely named "frontend")
   - Go to Settings → Environment Variables
   - Find the REACT_APP_API_URL variable
   - Update its value to your actual backend URL with /api suffix
   - Example: https://my-ai-todo-backend.onrender.com/api
   - Click Save

3. After updating the environment variable, redeploy your project:
   - Go to Deployments
   - Click the three dots menu on your latest deployment
   - Select "Redeploy"

Alternative method using Vercel CLI:
1. Run: vercel env rm REACT_APP_API_URL production (to remove old value)
2. Run: echo "https://your-actual-backend-url/api" | vercel env add REACT_APP_API_URL production

Note: Remember to include the "/api" suffix at the end of your backend URL since the frontend expects API endpoints at that path.