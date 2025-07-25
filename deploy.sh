#!/bin/bash

echo "🚀 Fresco Video Analysis Deployment Script"
echo "=========================================="

# Check if we're in the right directory
if [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Function to deploy frontend
deploy_frontend() {
    echo "📱 Deploying Frontend to Vercel..."
    cd frontend
    
    # Check if Vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
        echo "📦 Installing Vercel CLI..."
        npm install -g vercel
    fi
    
    # Deploy to Vercel
    echo "🚀 Starting Vercel deployment..."
    vercel --prod
    
    cd ..
    echo "✅ Frontend deployment initiated!"
}

# Function to show backend deployment options
show_backend_options() {
    echo ""
    echo "🔧 Backend Deployment Options:"
    echo "1. Railway (Recommended - Easy setup)"
    echo "2. Render (Good free tier)"
    echo "3. Heroku (Requires credit card)"
    echo "4. DigitalOcean App Platform"
    echo ""
    echo "Please choose your backend deployment platform and follow the instructions in DEPLOYMENT.md"
}

# Main deployment flow
echo "What would you like to deploy?"
echo "1. Frontend only (Vercel)"
echo "2. Show backend deployment options"
echo "3. Both (Frontend + Backend instructions)"

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        deploy_frontend
        ;;
    2)
        show_backend_options
        ;;
    3)
        deploy_frontend
        show_backend_options
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "📚 For detailed instructions, see DEPLOYMENT.md"
echo "🎉 Happy deploying!" 