#!/bin/bash

# Job Search Daily Planner - Startup Script

echo "🚀 Starting Job Search Daily Planner..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Navigate to backend directory
cd backend

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. You can customize it if needed."
fi

# Install dependencies
echo "📦 Installing dependencies..."
uv sync

# Run the application
echo "🎯 Starting the server..."
echo "📍 Web Interface: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uv run uvicorn app:app --reload --port 8000
