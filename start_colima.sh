#!/bin/bash

# Stop Colima and Docker services
echo "Stopping Docker services..."
docker-compose down
echo "Stopping Colima..."
colima stop

# Start Colima with mounts
echo "Starting Colima..."
colima start \
  --cpu 2 \
  --memory 4 \
  --mount ./files/:/team_2_files:w \
  --mount ./.n8n/:/my-n8n-files:w

# Start Docker services
echo "Starting Docker services..."
docker-compose up -d

echo "All services started successfully!"
echo "n8n is available at: http://localhost:5678"
echo "crawl4ai is available at: http://localhost:11235"