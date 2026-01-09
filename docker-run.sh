#!/bin/bash

# Docker Music Bot Runner Script
# This script helps you easily run the Discord music bot using Docker

set -e

IMAGE_NAME="discord-music-bot"
CONTAINER_NAME="discord-music-bot"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env file not found!"
    print_info "Please copy docker-env-example to .env and fill in your credentials:"
    echo "  cp docker-env-example .env"
    echo "  # Then edit .env with your Discord bot token and optional Spotify credentials"
    exit 1
fi

# Check if required environment variables are set
if ! grep -q "DISCORD_TOKEN=" .env || grep -q "DISCORD_TOKEN=your_" .env; then
    print_error "DISCORD_TOKEN not properly set in .env file!"
    print_info "Please edit .env and set your Discord bot token."
    exit 1
fi

print_info "Building Docker image..."
docker build -t $IMAGE_NAME .

print_info "Starting Discord Music Bot container..."
docker run -d \
    --name $CONTAINER_NAME \
    --env-file .env \
    --restart unless-stopped \
    $IMAGE_NAME

print_success "Discord Music Bot started successfully!"
print_info "Container name: $CONTAINER_NAME"
print_info ""
print_info "To view logs: docker logs -f $CONTAINER_NAME"
print_info "To stop the bot: docker stop $CONTAINER_NAME"
print_info "To restart: docker restart $CONTAINER_NAME"
print_info "To completely remove: docker rm -f $CONTAINER_NAME"