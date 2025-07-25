# Deployment Guide for Fresco Video Analysis

This guide covers deploying both the React frontend and FastAPI backend.

## Frontend Deployment (Vercel)

### Prerequisites
- Vercel account
- Node.js installed locally

### Steps

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

3. **Deploy to Vercel**:
   ```bash
   vercel
   ```

4. **Follow the prompts**:
   - Link to existing project or create new
   - Set project name
   - Confirm deployment settings

5. **Set environment variables** (after deployment):
   - Go to your Vercel dashboard
   - Navigate to your project settings
   - Add environment variable: `REACT_APP_API_URL` with your backend URL

### Alternative: Deploy via GitHub
1. Push your code to GitHub
2. Connect your repository to Vercel
3. Vercel will automatically deploy on pushes to main branch

## Backend Deployment Options

### Option 1: Railway (Recommended)
Railway is a great platform for Python applications with generous free tier.

1. **Create Railway account** at railway.app
2. **Connect your GitHub repository**
3. **Create new service** from GitHub repo
4. **Set environment variables**:
   - `GOOGLE_API_KEY`: Your Gemini API key
5. **Deploy** - Railway will automatically detect the Python app

### Option 2: Render
1. **Create Render account** at render.com
2. **Create new Web Service**
3. **Connect GitHub repository**
4. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Set environment variables**:
   - `GOOGLE_API_KEY`: Your Gemini API key

### Option 3: Heroku
1. **Create Heroku account**
2. **Install Heroku CLI**
3. **Create app**:
   ```bash
   heroku create your-app-name
   ```
4. **Add buildpack**:
   ```bash
   heroku buildpacks:set heroku/python
   ```
5. **Set environment variables**:
   ```bash
   heroku config:set GOOGLE_API_KEY=your_api_key
   ```
6. **Deploy**:
   ```bash
   git push heroku main
   ```

### Option 4: DigitalOcean App Platform
1. **Create DigitalOcean account**
2. **Create new app** in App Platform
3. **Connect GitHub repository**
4. **Configure as Python app**
5. **Set environment variables**
6. **Deploy**

## Environment Variables

### Frontend (Vercel)
- `REACT_APP_API_URL`: Your backend URL (e.g., https://your-backend.railway.app)

### Backend
- `GOOGLE_API_KEY`: Your Google Gemini API key

## Post-Deployment

1. **Update CORS settings** in `backend/main.py`:
   - Replace `"https://your-vercel-app.vercel.app"` with your actual Vercel domain

2. **Test the application**:
   - Upload a video file
   - Verify the analysis works
   - Check for any CORS errors

## Troubleshooting

### Common Issues

1. **CORS Errors**:
   - Ensure your backend CORS settings include your Vercel domain
   - Check that the frontend is using the correct API URL

2. **API Key Issues**:
   - Verify your Google API key is set correctly
   - Check that the key has access to Gemini API

3. **File Upload Issues**:
   - Check file size limits
   - Verify content-type headers

4. **Build Errors**:
   - Check that all dependencies are in requirements.txt
   - Verify Python version compatibility

## Monitoring

- **Vercel**: Check deployment logs and analytics
- **Backend Platform**: Monitor logs and performance
- **Google Cloud**: Monitor API usage and quotas

## Security Notes

- Never commit API keys to version control
- Use environment variables for all sensitive data
- Consider implementing rate limiting for production
- Add proper error handling and logging 