# workerNode
Builds an image of a worker node which returns a image with Delaunay traingles drawn over a person's face


Steps

1. Pull repo and open terminal in the project directory
2. Build Docker image with the command: docker build -t node:1.0 .
3. Create a container using the create image: docker run --name worker1 -d -p 5554:5554 -p 5556:5556 node:1.0
