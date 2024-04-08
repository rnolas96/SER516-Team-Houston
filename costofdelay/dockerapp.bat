@echo off

REM Pull Docker images
echo Pulling Docker images...
docker pull  rnolas96/prod-costofdelaymetric-backend:prod  
docker pull  rnolas96/prod-costofdelaymetric-frontend:prod  
docker pull redis:latest

REM Check if the pull was successful
if %errorlevel% neq 0 (
    echo Error: Failed to pull Docker images
    exit /b 1
)

REM Run Docker Compose to create containers
echo Creating containers...
docker-compose -p costofdelaymetricprod up -d