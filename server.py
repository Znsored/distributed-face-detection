import zmq
import numpy as np
import cv2
import json
import base64
from face import get_features
import time

def main():
    # Worker configuration
    server_address = "tcp://127.0.0.1:5554"
    worker_address = "tcp://127.0.0.1:5556"

    context = zmq.Context()

    # Create a PULL socket for receiving jobs from the server
    pull_socket = context.socket(zmq.PULL)
    pull_socket.connect(server_address)

    # Create a PUSH socket for sending acknowledgments to the server
    push_socket = context.socket(zmq.PUSH)
    push_socket.connect(worker_address)

    while True:
        # Receive the job (frame ID and image) from the server
        job_json = pull_socket.recv()
        job_data = json.loads(job_json.decode('utf-8'))

        # Extract frame ID and image from the received JSON
        frame_id = job_data['frame_id']
        image_base64 = job_data['image']

        # Decode the image from Base64
        image_data = base64.b64decode(image_base64)

        # Convert the image data to NumPy array
        image_array = np.frombuffer(image_data, dtype=np.uint8)

        # Decode the image array using OpenCV
        # image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # Process the image
        start_time = time.time()
        processed_image = get_features(image_array)
        end_time = time.time()
        time_taken = end_time - start_time
        print(time_taken)

        # Convert the processed image to grayscale
        # processed_image_gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
        #
        # # Encode the processed image5
        # _, processed_image_data = cv2.imencode('.jpg', processed_image)
        processed_image_base64 = base64.b64encode(processed_image).decode('utf-8')

        # Prepare the acknowledgment data in JSON format
        ack_data = {
            'frame_id': frame_id,
            'time_taken': time_taken,
            'worker_id': 1,
            'image': processed_image_base64
        }
        ack_json = json.dumps(ack_data)

        # Send the acknowledgment JSON back to the server
        push_socket.send(ack_json.encode())

    # Close the sockets and terminate the context
    pull_socket.close()
    push_socket.close()
    context.term()

if __name__ == "__main__":
    main()
