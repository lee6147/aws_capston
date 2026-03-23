#!/bin/bash
# StudyBot Development Startup Script
# Starts both mock API server and React frontend

echo "🤖 StudyBot Dev Server Starting..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Kill existing processes on ports
kill $(lsof -t -i:3001 2>/dev/null) 2>/dev/null
kill $(lsof -t -i:5173 2>/dev/null) 2>/dev/null

# Start mock server
echo -e "${BLUE}[1/2]${NC} Starting Mock API Server on port 3001..."
cd "$(dirname "$0")/backend"
python3 mock_server.py &
MOCK_PID=$!
sleep 2

# Verify mock server
if curl -s http://localhost:3001/api/documents > /dev/null 2>&1; then
    echo -e "${GREEN}  ✓ Mock server running${NC}"
else
    echo "  ✗ Mock server failed to start"
    exit 1
fi

# Start frontend
echo -e "${BLUE}[2/2]${NC} Starting React Frontend on port 5173..."
cd "$(dirname "$0")/frontend"
npm run dev -- --host &
FRONT_PID=$!
sleep 3

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  StudyBot is ready!${NC}"
echo -e "${GREEN}  Open: http://localhost:5173${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Press Ctrl+C to stop all servers"

# Trap Ctrl+C to kill both processes
trap "echo ''; echo 'Shutting down...'; kill $MOCK_PID $FRONT_PID 2>/dev/null; exit 0" INT

# Wait for either process to exit
wait
