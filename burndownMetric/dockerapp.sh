#!/bin/bash

# Pull frontend image
echo "Pulling avijay48/prod-burndownmetric-backend:prod..."
docker pull avijay48/prod-burndownmetric-backend:prod

# Pull backend image
echo "Pulling avijay48/prod-burndownmetric-backend:prod..."
docker pull avijay48/prod-burndownmetric-backend:prod

docker pull redis:latest

# Ensure docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
  echo "Error: docker-compose.yml not found!"
  exit 1
fi

# Start services in detached mode
echo "Starting services with docker-compose up -d..."
docker-compose -p burndownmetricprod up -d

echo "Done!"
