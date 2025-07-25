# Fresco Video Analysis

A React + FastAPI application that analyzes cooking videos using Google's Gemini AI to extract recipes.

## 🚀 Quick Deploy

### Frontend (Vercel)
```bash
# Run the deployment script
./deploy.sh

# Or deploy manually
cd frontend
npm install -g vercel
vercel --prod
```

### Backend (Railway - Recommended)
1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Create new service from the `backend` directory
4. Set environment variable: `GOOGLE_API_KEY=your_api_key`
5. Deploy!

## 📁 Project Structure

```
Fresco-video-analysis/
├── frontend/                 # React application
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vercel.json          # Vercel configuration
├── backend/                  # FastAPI application
│   ├── main.py              # Main API server
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Docker configuration
│   └── env.example         # Environment variables template
├── deploy.sh               # Deployment automation script
├── DEPLOYMENT.md           # Detailed deployment guide
└── README.md              # This file
```

## 🛠️ Local Development

### Prerequisites
- Node.js (v16+)
- Python (v3.8+)
- Google Gemini API key

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Fresco-video-analysis
   ```

2. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   
   # Set your API key
   export GOOGLE_API_KEY=your_api_key_here
   
   # Run the server
   uvicorn main:app --reload
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 🌐 Deployment Options

### Frontend
- **Vercel** (Recommended) - Best for React apps
- **Netlify** - Alternative to Vercel
- **GitHub Pages** - Free static hosting

### Backend
- **Railway** (Recommended) - Easy Python deployment
- **Render** - Good free tier
- **Heroku** - Requires credit card
- **DigitalOcean App Platform** - More control
- **AWS/GCP/Azure** - Enterprise options

## 🔧 Configuration

### Environment Variables

**Frontend (Vercel)**
- `REACT_APP_API_URL` - Your backend URL

**Backend**
- `GOOGLE_API_KEY` - Google Gemini API key

### CORS Settings
Update `backend/main.py` with your frontend domain:
```python
allow_origins=[
    "http://localhost:3000",
    "https://your-app.vercel.app"
]
```

## 📊 Features

- 🎥 Video upload and analysis
- 🍳 Recipe extraction using AI
- 📱 Responsive React interface
- 🔄 Real-time processing
- 📋 Structured recipe output

## 🚨 Limitations

- **Vercel Serverless Functions**: 10s timeout, 50MB payload limit
- **Video Size**: Large videos may need external processing
- **API Quotas**: Google Gemini has usage limits

## 🔍 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check backend CORS settings
   - Verify frontend API URL

2. **API Key Issues**
   - Ensure Google API key is valid
   - Check Gemini API access

3. **File Upload Problems**
   - Check file size limits
   - Verify video format support

4. **Build Errors**
   - Check Node.js/Python versions
   - Verify all dependencies installed

## 📈 Monitoring

- **Vercel Analytics**: Frontend performance
- **Backend Logs**: API usage and errors
- **Google Cloud Console**: API usage and quotas

## 🔒 Security

- API keys stored in environment variables
- CORS properly configured
- Input validation on file uploads
- Error handling without exposing sensitive data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For deployment issues:
1. Check the `DEPLOYMENT.md` file
2. Review the troubleshooting section
3. Check platform-specific documentation
4. Open an issue on GitHub

---

**Happy Cooking! 🍳** 