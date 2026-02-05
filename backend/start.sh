#!/bin/bash

echo "🚀 Starting GrowthPath Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check if database needs seeding
if [ ! -f "growthpath.db" ]; then
    echo "🌱 Seeding database with sample data..."
    python seed_data.py
fi

# Start the server
echo "✅ Starting FastAPI server on http://localhost:8000"
echo "📚 API Documentation available at http://localhost:8000/docs"
echo ""
python run.py
