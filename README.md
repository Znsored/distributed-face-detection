# Distributed Face Detection
A distributed system that detects faces in a video and draws Delaunay triangles over it.

## Features
### Easy Setup:
Seamless installation process through Docker images.
### Highly Scalable
Easily scale the number of worker nodes to match your desired workload with minimal configuration changes.
### Handles Multiple Tasks
Capable of efficiently handling multiple video requests simultaneously.
### Robust Logging
Incorporates comprehensive logging functionalities to track and monitor activities effectively.

## Instructions
1. Pull the repo and open the terminal in the project directory
2. Change directory to Kafka folder `cd kafka`
3. Run the docker compose file with the command `docker compose up -d`
4. Run the file `initialKafkaConfig.py` with the command `python initialKafkaConfig.py`
5. Change the directory to workerNode folder using the command `cd ../workerNode`
6. Change the IP address in the .env file to the IP address of the machine running Kafka.
7. Build a Docker image with the command: 
 `docker build -t node:1.0 .`
8. Change the machine ID as required in the .env file and build another docker image with the command: 
 `docker build -t node:1.1 .`
7. Create a container using the command `docker run --name worker1 -d -p 9090:9093 node:1.0` and `docker run --name worker2 -d -p 9099:9093 node:1.1` 
Now the message queue (Kafka) and two workers are ready.

8. Change to the machineNode folder using the command `cd ../machineNode`, and change the IP address in .env to the IP address of the machine running Kafka.
9. Run the `server.py` to host the website in `localhost:5000`, upload the video and click send. 
10. The resulting video will be displayed after a few seconds with complete statistics.

## License
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/Znsored/workerNode/blob/main/LICENSE)
