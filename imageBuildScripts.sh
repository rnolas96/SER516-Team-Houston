#!/bin/bash
# Run Docker Compose to create sbpbCoupling containers

echo "Building microservices images..."

# Build sbpbCoupling backend
docker build -t sbpbcouping-metric-backend ./sbpbcoupling/backend

# Build sbpbCoupling frontend
docker build -t sbpbcouping-metric-frontend ./sbpbcoupling/frontend

# Build engagement metric backend
docker build -t engagement-metric-backend ./engagementmetric/backend

# Build engagement metric frontend
docker build -t engagement-metric-frontend ./engagementmetric/frontend

# Build burndown metric backend
docker build -t burndown-metric-backend ./burndownmetric/backend

# Build burndown metric frontend
docker build -t burndown-metric-frontend ./burndownmetric/frontend

# Build cost of delay metric backend
docker build -t costofdelay-metric-backend ./costofdelay/backend

# Build cost of delay metric frontend
docker build -t costofdelay-metric-frontend ./costofdelay/frontend

# Build cycle time metric backend
docker build -t cycletime-metric-backend ./cycletime/backend

# Build cycle time metric frontend
docker build -t cycletime-metric-frontend ./cycletime/frontend

# Build lead time metric backend
docker build -t leadtime-metric-backend ./leadtime/backend

# Build lead time metric frontend
docker build -t leadtime-metric-frontend ./leadtime/frontend

# Build task coupling metric backend
docker build -t taskcoupling-metric-backend ./taskcoupling/backend

# Build task coupling metric frontend
docker build -t taskcoupling-metric-frontend ./taskcoupling/frontend

# Build demo app frontend
docker build -t demoapp-frontend ./demoApp/frontend

echo "Successfully built all the microservices images"

read -p "Press Enter to start containers..."

# Start containers
docker run -d sbpbcouping-metric-backend
docker run -d sbpbcouping-metric-frontend
docker run -d engagement-metric-backend
docker run -d engagement-metric-frontend
docker run -d burndown-metric-backend
docker run -d burndown-metric-frontend
docker run -d costofdelay-metric-backend
docker run -d costofdelay-metric-frontend
docker run -d cycletime-metric-backend
docker run -d cycletime-metric-frontend
docker run -d leadtime-metric-backend
docker run -d leadtime-metric-frontend
docker run -d taskcoupling-metric-backend
docker run -d taskcoupling-metric-frontend
docker run -d demoapp-frontend
