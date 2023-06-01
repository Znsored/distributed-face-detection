import zmq
from faceDetector import get_features
import os

string_template = "tcp://{ip}:{port}"

in_ip = os.getenv("IN_IP")
out_ip = os.getenv("OUT_IP")
in_port = os.getenv("IN_PORT")
out_port = os.getenv("OUT_PORT")



def main():
    # Worker configuration
    server_address = string_template.format(ip=in_ip, port=in_port)
    worker_address = string_template.format(ip=out_ip, port=out_port)

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
