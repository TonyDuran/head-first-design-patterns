#!/bin/bash

# Observer Pattern Demo - Run Script

echo "🐍 Observer Pattern Snake Game Demo"
echo "===================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "⚠️  Using 'docker compose' (newer version)"
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo "🚀 Starting Observer Pattern Demo..."
echo ""
echo "📍 Access the demo at:"
echo "   Player (Game Controller): http://localhost:8000/player"
echo "   Spectators (Watchers):    http://localhost:8000/"
echo ""
echo "🔗 To access from other machines on your network:"
echo "   Replace 'localhost' with your machine's IP address"
echo "   Find your IP: ifconfig | grep inet"
echo ""

$DOCKER_COMPOSE up

