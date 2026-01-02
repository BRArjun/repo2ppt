#!/bin/bash

# HackDeck Quick Start Script

echo "🚀 Starting HackDeck..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env created. Please edit it with your API keys before continuing."
    echo ""
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p temp_repos logs

echo ""
echo "✅ Setup complete!"
echo ""
echo "Starting services..."
echo ""

# Start FastAPI backend in background
echo "🔷 Starting FastAPI backend..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start Streamlit frontend
echo "🔶 Starting Streamlit frontend..."
streamlit run app/frontend/streamlit_app.py &
FRONTEND_PID=$!

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ HackDeck is running!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔷 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🔶 Frontend: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for user interrupt
trap "echo ''; echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit 0" INT

# Keep script running
wait