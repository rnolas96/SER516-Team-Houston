
#!/bin/bash

# Pull frontend image
echo "Pulling akashvj98/taigafrontend:dev..."
docker pull akashvj98/taigafrontend:dev

# Pull backend image
echo "Pulling akashvj98/taigabackend:dev..."
docker pull akashvj98/taigabackend:dev

# Ensure docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
  echo "Error: docker-compose.yml not found!"
  exit 1
fi

# Start services in detached mode
echo "Starting services with docker-compose up -d..."
docker-compose up -d

echo "Done!"
