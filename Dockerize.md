# Dockerize Flask Application

## Docker Setup
https://docs.docker.com/desktop/install/windows-install/

## Setup
1. To build requirements.txt: ```pip freeze > requirements.txt```
    - Note: This will pull all packages installed with pip, to generate only required:
      - ```pip install pipreqs```
      - ```pipreqs .```
2. Create Dockerfile (sample included in this package)
3. To build docker image: ```docker build -t web-ptt .```
4. To save: ```docker save -o web-ptt.tar web-ptt```
5. Transfer .tar file to another machine
6. To load docker image: ```docker load -i web-ptt.tar```
7. To run: ```docker run -d -p 5001:5001 web-ptt```