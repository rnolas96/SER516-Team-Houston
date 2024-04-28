@echo off

echo  _____                         _   _                     _                
echo ^|_   _^|                       ^| ^| ^| ^|                   ^| ^|               
echo   ^| ^|  ___   __ _  _ __ ___   ^| ^|_^| ^|  ___   _   _  ___ ^| ^|_  ___   _ __  
echo   ^| ^| / _ \ / _` ^|^| '_ ` _ \  ^|  _  ^| / _ \ ^| ^| ^| ^|/ __^|^| __^|/ _ \ ^| '_ \ 
echo   ^| ^|^|  __/^| (_^| ^|^| ^| ^| ^| ^| ^| ^| ^| ^| ^|^| (_) ^|^| ^|_^| ^|\__ \^| ^|_^| (_) ^|^| ^| ^| ^|
echo   \_/ \___^| \__,_^|^|_^| ^|_^| ^|_^| \_^| ^|_/ \___/  \__,_^|^|___/ \__^|\___/ ^|_^| ^|_^|                                                                        

REM Run Docker Compose to create sbpbCoupling containers
echo Building microservices images...

REM Build sbpbCoupling backend
docker build -t sbpbcouping-metric-backend ./sbpbcoupling/backend

REM Build sbpbCoupling frontend
docker build -t sbpbcouping-metric-frontend ./sbpbcoupling/frontend

REM Build engagement metric backend
docker build -t engagement-metric-backend ./engagementmetric/backend

REM Build engagement metric frontend
docker build -t engagement-metric-frontend ./engagementmetric/frontend

REM Build burndown metric backend
docker build -t burndown-metric-backend ./burndownmetric/backend

REM Build burndown metric frontend
docker build -t burndown-metric-frontend ./burndownmetric/frontend

REM Build cost of delay metric backend
docker build -t costofdelay-metric-backend ./costofdelay/backend

REM Build cost of delay metric frontend
docker build -t costofdelay-metric-frontend ./costofdelay/frontend

REM Build cycle time metric backend
docker build -t cycletime-metric-backend ./cycletime/backend

REM Build cycle time metric frontend
docker build -t cycletime-metric-frontend ./cycletime/frontend

REM Build lead time metric backend
docker build -t leadtime-metric-backend ./leadtime/backend

REM Build lead time metric frontend
docker build -t leadtime-metric-frontend ./leadtime/frontend

REM Build task coupling metric backend
docker build -t taskcoupling-metric-backend ./taskcoupling/backend

REM Build task coupling metric frontend
docker build -t taskcoupling-metric-frontend ./taskcoupling/frontend

REM Build demo app frontend
docker build -t demoapp-frontend ./demoApp/frontend

echo Successfully built all the microservices images

pause




docker run -d ^
    --name cycletime-api-container ^
    -e TAIGA_URL=https://api.taiga.io/api/v1 ^
    -p 8085:8000 ^
    cycletime-metric-backend
docker run -d ^
--name cycletime-redis-container ^
-p 6385:6379 ^
-v prod-cycletime-redis_data:/data ^
redis
docker run -d ^
    --name cycletime-gui-container ^
    -p 3035:80 ^
    --link cycletime-api-container ^
   cycletime-metric-frontend




docker run -d ^
    --name api-container-burndown ^
    -e TAIGA_URL=https://api.taiga.io/api/v1 ^
    -p 8080:8000 ^
     burndown-metric-backend
docker run -d ^
--name burndown-redis-container ^
-p 6370:6379 ^
-v prod-burndown-redis_data:/data ^
redis

docker run -d ^
    --name  gui-container-burndown ^
    -p 3000:80 ^
    --link api-container-burndown ^
 burndown-metric-frontend






 docker run -d ^
    --name taskcoupling-api-container ^
    -e TAIGA_URL=https://api.taiga.io/api/v1 ^
    -p 8084:8000 ^
    taskcoupling-metric-backend
     



docker run -d ^
    --name taskcoupling-gui-container ^
    -p 3004:80 ^
    --link taskcoupling-api-container ^
taskcoupling-metric-frontend

 docker run -d ^
    --name leadime-api-container ^
    -e TAIGA_URL=https://api.taiga.io/api/v1 ^
    -p 8086:8000 ^
      leadtime-metric-backend



docker run -d ^
    --name leadtime-gui-container ^
    -p 3036:80 ^
    --link leadime-api-container ^
 leadtime-metric-frontend



 docker run -d ^
    --name  sbpbcoupling-api-container ^
    -e TAIGA_URL=https://api.taiga.io/api/v1 ^
    -p 8082:8000 ^
	sbpbcouping-metric-backend


docker run -d ^
    --name sbpbcoupling-gui-container ^
    -p 3002:80 ^
    --link  sbpbcoupling-api-container ^
 sbpbcouping-metric-frontend

 
 docker run -d ^
    --name  api-container-costofdelay ^
    -e TAIGA_URL=https://api.taiga.io/api/v1 ^
    -p 8081:8000 ^
	costofdelay-metric-backend

docker run -d ^
--name redis-container-costofdelay ^
-p 6369:6379 ^
-v  prod-redis_data:/data ^
redis


docker run -d ^
    --name gui-container-costofdelay ^
    -p 3006:80 ^
    --link api-container-costofdelay ^
 costofdelay-metric-frontend

 
 docker run -d ^
    --name  api-container-engagement ^
    -e TAIGA_URL=https://api.taiga.io/api/v1 ^
    -p 8005:8000 ^
	engagement-metric-backend



docker run -d ^
    --name  gui-container-engagement ^
    -p 3005:80 ^
    --link api-container-engagement ^
engagement-metric-frontend

docker run -d ^
    --name  gui-container-demoapp ^
    -p 3001:80 ^
   demoapp-frontend
