#!/bin/bash

# SDN302 AI Assistant Startup Script

echo "🚀 Starting SDN302 AI Assistant..."

# Check if Python and dependencies are installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check environment variables
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  No GITHUB_TOKEN environment variable found."
    echo "💡 The app will run in demo mode with mock responses."
    echo "   To use full AI capabilities, set GITHUB_TOKEN environment variable."
fi

# Run the Streamlit app
echo "🌐 Starting Streamlit application..."
echo "📍 App will be available at http://localhost:8501"

streamlit run app.py