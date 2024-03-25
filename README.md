# SER516-Team-Houston

#  Instruction to run the app


## Prerequisites

Before running the script, make sure you have the following installed:

-Docker Desktop / Hub

## windows users:
 click on the dockerapp.bat file in the taigaproject directory.

 The script will pull the images of backend, frontend and redis from the public repository.
 Then it will execute the docker-compose up to create and start the containers according to the configurations in docker-compose.yml.


## Ubuntu / Mac users:
   chmod +x dockerapp.sh


** note : Once the containers start up,  click on the port-no of the frontend-container here (localhost:3000).
