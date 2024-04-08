# DEV BRANCH CODE

## PURPOSES

- ### Integration testing is conducted here 

- ### Once a completed user story is achieved, the user story branch is merged into the dev branch.

- ### The dev branch will act as the final buffer to the main branch. Once the integration testing is completed, the code is pushed to the main branch

## SETTING UP DEV CODE

### 1. Node setup

- ### Ubuntu steps

    - ``` curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash ```

    -  ``` source ~/.bashrc ```

    - ``` nvm install --lts ```

    - ``` nvm alias default <VERSION BEING INSTALLED> ```

    - Verify with ``` node -v npm -v ```

- ### WINDOWS steps

    - (To be added)

### 2. Running python code

- Same process given on the project README. 

- For testing with FAST API, deploy python code like so,

   ```python -m uvicorn main:app ``` 

### 3. Running react code

- ### npm start

- ``` http://localhost:3000 ```

### 4. Docker Setup

- # docker-compose up -d



