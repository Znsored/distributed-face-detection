import zmq
from faceDetector import get_features

def main():
    # Worker configuration
    server_address = "tcp://10.0.0.87:5554"
    worker_address = "tcp://10.0.0.87:5556"

    context = zmq.Context()

    # Create a PULL socket for receiving jobs from the server
    pull_socket = context.socket(zmq.PULL)
    pull_socket.connect(server_address)

    # Create a PUSH socket for sending acknowledgments to the server
    push_socket = context.socket(zmq.PUSH)
    push_socket.connect(worker_address)

    while True:
        # Receive the job (image) from the server
        image_data = pull_socket.recv()
        ack_data=get_features(image_data)
        push_socket.send(ack_data)

    # Close the sockets and terminate the context
        pull_socket.close()
        push_socket.close()
        context.term()

if __name__ == "__main__":
    main()
