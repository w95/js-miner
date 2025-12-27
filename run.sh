#!/bin/bash

# JS Miner FastAPI - Run Script

echo "Starting JS Miner FastAPI..."
echo "================================"

# Check Python version
if ! command -v python3.10 &> /dev/null; then
    echo "Python 3.10 not found. Please install Python 3.10+"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.10 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy .env if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
fi

# Run the application
echo "Starting FastAPI server..."
echo "API will be available at: http://localhost:8000"
echo "Documentation: http://localhost:8000/docs"
echo "================================"

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
