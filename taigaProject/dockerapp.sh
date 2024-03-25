#!/bin/bash

# Pull frontend image
echo "Pulling avijay48/periodtwo-taigaproject-frontend:periodtwo"
docker pull avijay48/periodtwo-taigaproject-frontend:periodtwo

# Pull backend image
echo "Pulling ...avijay48/periodtwo-taigaproject-backend:periodtwo"
docker pull avijay48/periodtwo-taigaproject-backend:periodtwo

#pull redis image
echo "Pulling redis image..."
docker pull redis:latest


# Ensure docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
  echo "Error: docker-compose.yml not found!"
  exit 1
fi

# Start services in detached mode
echo "Starting services with docker-compose up -d..."
docker-compose up -d

echo "Done!"