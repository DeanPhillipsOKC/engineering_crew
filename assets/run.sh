#!/bin/bash

IMAGE_NAME=streamlit-app
CONTAINER_NAME=streamlit-ui

# Build the Docker image
docker build -t $IMAGE_NAME .

# Stop and remove any existing container with the same name
docker rm -f $CONTAINER_NAME 2>/dev/null

# Run the container, mapping port 8501
docker run -d \
    --name $CONTAINER_NAME \
    -p 8501:8501 \
    $IMAGE_NAME

echo "Streamlit UI is running at http://localhost:8501"