import zmq
import logging
import json
import base64
import time
from faceDetector import get_features
from dotenv import dotenv_values

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
    
    # Create a PULL socket for receiving jobs from the server
    pull_socket = context.socket(zmq.PULL)
    pull_socket.connect(server_address)

    # Create a PUSH socket for sending acknowledgments to the server
    push_socket = context.socket(zmq.PUSH)
    push_socket.connect(worker_address)

    logging.info("Connection Established")

    while True:
        logging.info("Waiting for Image")
        # Receive the job (image) from the server

        job_json = pull_socket.recv()
        job_data = json.loads(job_json.decode('utf-8'))

        logging.info("Received Image. Processing...")
        # Extract frame ID and image from the received JSON
        frame_id = job_data['frame_id']
        image_base64 = job_data['image']

        # Decode the image from Base64
        image_data = base64.b64decode(image_base64)

        start_time = time.time()
        processed_image = get_features(image_data)
        end_time = time.time()
        
        logging.info("Features Extracted, Sending Message")
        
        time_taken = end_time - start_time
        processed_image_base64 = base64.b64encode(processed_image).decode('utf-8')

        # Prepare the acknowledgment data in JSON format
        ack_data = {
            'frame_id': frame_id,
            'time_taken': time_taken,
            'worker_id': 1,
            'image': processed_image_base64
        }
        ack_json = json.dumps(ack_data)


        push_socket.send(ack_json.encode())
        logging.info("Successfully Sent Image")

if __name__ == "__main__":
    main()
