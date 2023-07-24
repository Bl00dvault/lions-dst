# Dockerize Flask Application

## Docker Setup
https://docs.docker.com/desktop/install/windows-install/

## Setup
1. To build requirements.txt:   
```pip freeze > requirements.txt```
    - Note: This will pull all packages installed with pip, to generate only required:
      - ```pip install pipreqs```
      - ```pipreqs .```
2. Create Dockerfile (sample included in this package)
3. To build docker image:  
```docker build -t web-ptt .```
4. To save:  
```docker save -o web-ptt.tar web-ptt```
5. Transfer .tar file to another machine
6. To load docker image:  
```docker load -i web-ptt.tar```
7. Copy static files to the new machine (/static/academics folder)
8. To run:  
 ```docker run -v ~/lion-web-ptt/academics:/app/static/academics -v ~/lion-web-ptt/db:/app/db -v ~/lion-web-ptt/scores:/app/scores -p 5001:5001 -d web-ptt```

## Adding/Changing Academics/Exercises
- To change exercise questions, edit exercise.json in ~/lion-web-ptt/academics/, save, stop the container, start the container. The exercise will be updated
- To add/change academics, make sure the academics are in the correct home directory (the home directory of the user who started the docker container [will be root if you used sudo]), place a file with 'Exercise_Name'-Academics.pdf or 'Exercise_Name'-Lab.pdf where exercise_name is the same name from the top level of the exercise.json, and refresh the page. This should not require a container restart.
    - You can have multiple labs and academics render, but academics must end with 'Academics.pdf' and labs must start with 'Exercise_Name-Lab' and end with .pdf

 ## Troubleshooting
- If you get an error that the port is already in use, you can find the process using the port with:
   - ```netstat -ano | findstr :5001```
   - ```taskkill /PID <PID> /F```

- If vmmem is using a lot of memory you can stop it with:
   - ```wsl --shutdown```

- When adding new exercises/academics files you'll need to restart the docker container:
   - ```docker ps```
   - ```docker stop <CONTAINER ID>```
   - ```docker start <CONTAINER ID>```
- Troubleshoot container start
   - docker logs <CONTAINER ID/INSTANCE ID>
