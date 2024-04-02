
#!/bin/bash

# Pull frontend image
echo "Pulling avijay48/dev-taigaproject-backend:dev..."
docker pull avijay48/dev-taigaproject-backend:dev

# Pull backend image
echo "Pulling avijay48/dev-taigaproject-backend:dev..."
docker pull avijay48/dev-taigaproject-backend:dev

docker pull redis:latest

# Ensure docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
  echo "Error: docker-compose.yml not found!"
  exit 1
fi

# Start services in detached mode
echo "Starting services with docker-compose up -d..."
docker-compose -p taigaprojectdev up -d

echo "Done!"
