import zmq
from faceDetector import get_features
from dotenv import dotenv_values
import logging

string_template = "tcp://{ip}:{port}"
env_vars = dotenv_values('.env')

in_ip = env_vars["IN_IP"]
out_ip = env_vars["OUT_IP"]
in_port = env_vars["IN_PORT"]
out_port = env_vars["OUT_PORT"]

logging.basicConfig(level=logging.INFO)

def main():
    # Worker configuration
    server_address = string_template.format(ip=in_ip, port=in_port)
    worker_address = string_template.format(ip=out_ip, port=out_port)

    context = zmq.Context()
    logging.info("running")
    # Create a PULL socket for receiving jobs from the server
    pull_socket = context.socket(zmq.PULL)
    pull_socket.connect(server_address)

    # Create a PUSH socket for sending acknowledgments to the server
    push_socket = context.socket(zmq.PUSH)
    push_socket.connect(worker_address)

    while True:
        logging.info("Waiting for Image")
        # Receive the job (image) from the server
        image_data = pull_socket.recv()
        logging.info("Received Image, getting features")
        ack_data=get_features(image_data)
        logging.info("Features Extracted")
        push_socket.send(ack_data)
        logging.info("Successfully Sent Image")

if __name__ == "__main__":
    main()
