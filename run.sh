#!/bin/bash

echo "Starting Trekking Management Application..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Run the application
echo ""
echo "============================================"
echo "Trekking Management Application"
echo "============================================"
echo ""
echo "Starting Flask server..."
echo "Application URL: http://localhost:5000"
echo ""
echo "Default Admin Login:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Press CTRL+C to stop the server"
echo "============================================"
echo ""

python app.py
