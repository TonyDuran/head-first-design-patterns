#!/bin/bash

# Simple script to run the Strategy Pattern demo locally

echo "🚀 Starting Strategy Pattern Demo..."
echo ""
echo "This will start:"
echo "  - Backend API on http://localhost:8000"
echo "  - Frontend UI on http://localhost:8080"
echo ""

# Check if requirements are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
fi

echo "🔧 Starting backend server..."
cd backend
python main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

echo "🎨 Starting frontend server..."
cd ../frontend
python -m http.server 8080 &
FRONTEND_PID=$!

echo ""
echo "✅ Application is running!"
echo ""
echo "📍 Access the application at:"
echo "   Frontend: http://localhost:8080"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop..."

# Handle shutdown
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM

# Wait for processes
wait
