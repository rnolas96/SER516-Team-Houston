@echo off
REM Pull docker images


docker pull redis

echo Pulling Burndown microservices images...
docker pull  vshar17/burndown-metric-backend-img:prod  
docker pull  vshar17/burndown-metric-frontend-img:prod


echo Pulling taskcoupling microservices images...
docker pull avijay48/taskcoupling-backend-img:prod   
docker pull avijay48/taskcoupling-frontend-img:prod 


echo Pulling sbpbcoupling microservices images...
docker pull  avijay48/sbpbcoupling-backend-img:prod  
docker pull  avijay48/sbpbcoupling-frontend-img:prod


echo Pulling costofdelay microservice images...
docker pull vshar17/costofdelay-metric-backend-img:prod
docker pull vshar17/costofdelay-metric-frontend-img:prod 

echo Pulling engagementmetric microservice images...
docker pull vshar17/engagement-metric-backend-img:prod
docker pull vshar17/engagement-metric-frontend-img:prod 


echo Pulling cycletime microservice images...
docker pull rnolas96/cycletime-backend-img:prod   
docker pull rnolas96/cycletime-frontend-img:prod 


echo Pulling leadtime microservice images...
docker pull rnolas96/leadtime-backend-img:prod
docker pull rnolas96/leadtime-frontend-img:prod

REM Check if the pull was successful
if %errorlevel% neq 0 (
    echo Error: Failed to pull Docker images
    exit /b 1
)

REM Run Docker Compose to create burndownMetric containers
echo Creating burndown container...
cd burndownMetric
docker-compose up -d
cd..

REM Run Docker Compose to create leadtime containers
echo Creating leadtime container...
cd leadtime 
docker-compose up -d
cd..


REM Run Docker Compose to create cycletime containers
echo Creating cycletime container...
cd cycletime 
docker-compose up -d
cd..


REM Run Docker Compose to create costofdelay containers
echo Creating costofdelay container...
cd costofdelay 
docker-compose up -d
cd..


REM Run Docker Compose to create taskcoupling containers
echo Creating taskcoupling container...
cd taskcoupling
docker-compose -p taskcoupling up -d
cd..


REM Run Docker Compose to create engagementmetric containers
echo Creating engagementmetric container...
cd engagementmetric 
docker-compose up -d
cd..


REM Run Docker Compose to create sbpbCoupling containers
echo Creating sbpbCoupling container...
cd sbpbcoupling
docker-compose  up -d
cd..

echo "successfully created all the containers"

pause
