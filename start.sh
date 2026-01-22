#!/bin/bash

# Newla AI Startup Script

echo "=================================="
echo "Newla AI Startup"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found!"
    echo "Creating .env from template..."
    cp .env.example .env
    echo "Please edit .env and add your API keys"
    echo ""
    read -p "Press Enter to continue (or Ctrl+C to exit and configure .env)..."
fi

# Start the server
echo ""
echo "=================================="
echo "Starting Newla AI Server"
echo "=================================="
echo ""

cd backend
python main.py