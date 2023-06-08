# Distributed Face Detection
A distributed systems that detects face in a video and draws delaunay traingles over it.


## Instructions
1. Pull repo and open terminal in the project directory
2. Change directory to kafka folder `cd kafka`
3. Run the docker complse file with the command `docker compose up -d`
4. Run the file `initialKafkaConfig.py` with the command `python initialKafkaConfig.py`
5. Change directory to workerNode folder using the command `cd ../workerNode`
6. Change the ip address in .env file to the IP address of the machine running kafka.
7. Build Docker image with the command: 
 `docker build -t node:1.0 .`
8. Change machine ID as required in the .env file and build another docker image with the command: 
 `docker build -t node:1.1 .`
7. Create a containers using the command `docker run --name worker1 -d -p 9090:9093 node:1.0` and `docker run --name worker2 -d -p 9099:9093 node:1.1` 
*Now the message queue (kafka) and two workers are ready*
8. Change to machineNode folder using the command `cd ../machineNode`, change IP address in .env to the IP address of the machine running kafka.
9. Run the `server.py` to host the website in `localhost:5000`, upload the video and click send. 
10. The result video will be displayed after a few seconds with complete statistics.

## License
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/Znsored/workerNode/blob/main/LICENSE)
