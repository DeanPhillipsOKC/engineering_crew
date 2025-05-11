#!/bin/bash
set -e

# Build and run the Streamlit Docker container from the current directory
# Usage: ./run_streamlit.sh

IMAGE_NAME="streamlit-ui-demo:latest"
CONTAINER_NAME="streamlit-ui-demo-container"
HOST_PORT=8501
CONTAINER_PORT=8501

# Check that docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH. Please install Docker to use this script."
    exit 1
fi

# Build the Docker image

echo "Building Docker image ($IMAGE_NAME)..."
docker build -t "$IMAGE_NAME" .

echo "Removing any existing container named $CONTAINER_NAME (if running)..."
docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

echo "Running Streamlit UI in Docker container on http://localhost:$HOST_PORT ..."
docker run --name "$CONTAINER_NAME" -p $HOST_PORT:$CONTAINER_PORT --rm "$IMAGE_NAME"
