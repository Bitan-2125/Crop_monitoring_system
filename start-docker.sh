#!/bin/bash

# Harvestify Docker Quick Start Script

echo "🚀 Starting Harvestify with Docker..."

# Check if .env file exists
if [ ! -f "app/.env" ]; then
    echo "⚠️  Warning: app/.env file not found!"
    echo "Creating from app/.env.example..."
    if [ -f "app/.env.example" ]; then
        cp app/.env.example app/.env
        echo "✅ Created app/.env - Please edit it with your API keys"
        exit 1
    else
        echo "❌ app/.env.example not found. Please create app/.env manually"
        exit 1
    fi
fi

# Build Docker image
echo "📦 Building Docker image..."
docker build -t harvestify:latest .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed!"
    exit 1
fi

echo "✅ Docker image built successfully!"

# Stop and remove existing container if running
if [ "$(docker ps -aq -f name=harvestify-app)" ]; then
    echo "🛑 Stopping existing container..."
    docker stop harvestify-app
    docker rm harvestify-app
fi

# Run the container
echo "🏃 Starting container..."
docker run -d \
    --name harvestify-app \
    -p 8000:8000 \
    --env-file app/.env \
    --restart unless-stopped \
    harvestify:latest

if [ $? -eq 0 ]; then
    echo "✅ Container started successfully!"
    echo ""
    echo "🌐 Access your app at: http://localhost:8000"
    echo ""
    echo "📋 Useful commands:"
    echo "  View logs:    docker logs -f harvestify-app"
    echo "  Stop app:     docker stop harvestify-app"
    echo "  Restart app:  docker restart harvestify-app"
    echo "  Remove app:   docker rm -f harvestify-app"
    echo ""
    echo "Showing logs (Ctrl+C to exit)..."
    sleep 2
    docker logs -f harvestify-app
else
    echo "❌ Failed to start container!"
    exit 1
fi
