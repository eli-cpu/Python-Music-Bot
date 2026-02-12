#!/bin/bash

# Quick start script for Spotify Wrapper
# This script helps you get started with the development environment

set -e

echo "🎵 Spotify Wrapper - Quick Start Script"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi
echo "✓ Node.js found: $(node --version)"

# Check npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi
echo "✓ npm found: $(npm --version)"

echo ""
echo "📦 Installing dependencies..."
echo ""

# Install backend dependencies
echo "1. Installing backend dependencies..."
cd backend
python3 -m pip install -q -r requirements.txt
cd ..
echo "✓ Backend dependencies installed"

# Install frontend dependencies
echo "2. Installing frontend dependencies..."
cd frontend
npm install --silent
cd ..
echo "✓ Frontend dependencies installed"

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the services:"
echo ""
echo "1. Backend (Terminal 1):"
echo "   cd backend && python app.py"
echo ""
echo "2. Frontend (Terminal 2):"
echo "   cd frontend && npm start"
echo ""
echo "3. Discord Bot (Terminal 3):"
echo "   python bot.py"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT.md"
echo ""
