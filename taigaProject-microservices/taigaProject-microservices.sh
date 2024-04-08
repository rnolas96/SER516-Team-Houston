#!/bin/bash

# Pull Docker images
echo "Pulling Docker images..."
docker pull redis
docker pull vshar17/burndown-metric-backend-img:prod
docker pull vshar17/burndown-metric-frontend-img:prod
docker pull avijay48/taskcoupling-backend-img:prod
docker pull avijay48/taskcoupling-frontend-img:prod
docker pull avijay48/sbpbcoupling-backend-img:prod
docker pull avijay48/sbpbcoupling-frontend-img:prod
docker pull vshar17/costofdelay-metric-backend-img:prod
docker pull vshar17/costofdelay-metric-frontend-img:prod
docker pull vshar17/engagement-metric-backend-img:prod
docker pull vshar17/engagement-metric-frontend-img:prod
docker pull rnolas96/cycletime-backend-img:prod
docker pull rnolas96/cycletime-frontend-img:prod
docker pull rnolas96/leadtime-backend-img:prod
docker pull rnolas96/leadtime-frontend-img:prod

# Check if the pull was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to pull Docker images"
    exit 1
fi

# Run Docker Compose for each service
echo "Creating burndown container..."
cd burndownMetric || exit
docker-compose up -d
cd ..

echo "Creating leadtime container..."
cd leadtime || exit
docker-compose up -d
cd ..

echo "Creating cycletime container..."
cd cycletime || exit
docker-compose up -d
cd ..

echo "Creating costofdelay container..."
cd costofdelay || exit
docker-compose up -d
cd ..

echo "Creating taskcoupling container..."
cd taskcoupling || exit
docker-compose -p taskcoupling up -d
cd ..

echo "Creating engagementmetric container..."
cd engagementmetric || exit
docker-compose up -d
cd ..

echo "Creating sbpbCoupling container..."
cd sbpbcoupling || exit
docker-compose up -d
cd ..

echo "Successfully created all the containers"