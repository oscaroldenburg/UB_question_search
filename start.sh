#!/bin/bash

# Navigate to the script's directory
cd "$(dirname "$0")"

cd api

# Activate virtual environment
source .venv/bin/activate

echo "Starting backend on http://localhost:8000"
# Start uvicorn server in background
uvicorn api:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Navigate to frontend directory
cd ../ui

echo "Starting frontend on http://localhost:5173"
# Start frontend dev server
npm run dev &
FRONTEND_PID=$!

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Trap Ctrl+C and call cleanup
trap cleanup INT TERM

echo ""
echo "Both servers are running!"
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for both processes
wait
