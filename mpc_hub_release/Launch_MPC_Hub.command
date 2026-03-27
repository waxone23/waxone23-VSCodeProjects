#!/bin/bash

# Navigate to the folder where this script is located
cd "$(dirname "$0")"

echo "------------------------------------------------"
echo "🎹 Launching MPC Sample Hub Pro..."
echo "------------------------------------------------"

# 1. Clean up old sessions
docker stop mpc-hub 2>/dev/null
docker rm mpc-hub 2>/dev/null

# 2. Build the latest version
echo "📦 Building Hub..."
docker build -t mpc-hub .

# 3. Launch with the NEW volume mapping
echo "🚀 Starting server..."
docker run -d \
  -p 8000:8000 \
  -v ~/Music/MPC_Samples:/app/MPC_Samples \
  --name mpc-hub \
  mpc-hub

# 4. Open the browser
sleep 2
open http://localhost:8000

echo "✅ Success! Hub is live. Check ~/Music/MPC_Samples for your files."