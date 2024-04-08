# SER516-Team-Houston

#  Instruction to run the app


## Prerequisites

Before running the script, make sure you have the following installed:

-Docker Desktop / Hub

### step 1: 
**goto SER516-Team-Houston**
### step 2: 
**open the taigaProject-microservices directory**
the taigaProject-microservices has all the docker-compose.yml files and the scripts to pull the docker images and create containers.

### windows users:
 Double click on the **taigaProject-microservices.bat** file which is present in the taigaproject directory  in file explorer and then double click on the dockerapp.bat file.

 The .bat file(batch) will pull the images of backend, frontend and redis from the public repository.
 Then it will execute the docker-compose up to create and start the containers according to the configurations in docker-compose.yml.


### Ubuntu / Mac users:

### step 3 ###
  ``` chmod +x taigaProject-microservices.sh ```
### step 4 ###
  ``` ./taigaProject-microservices.sh ```


 The script will pull the images of backend, frontend and redis from the public repository.
 Then it will execute the docker-compose up to create and start the containers according to the configurations in docker-compose.yml.

#### step 5 : 
**Once the containers start up,  goto docker desktop and click on the port-no 3001 of the demoApp.**

**you will be redirected to the login page**

###  step 6 : 
**enter the username and password of your taiga account**

### step 7 : 
**obtain project slug , paste it in the text box provided and then click on submit.**
### step 8 : 
**select the sprint from the dropdown and then you will get the burndown charts for that spring**

### Note  other microservices can also be tested by following the same steps mentioned above.
