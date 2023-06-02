import time
import zmq
import cv2
import numpy as np
import os
import json
import base64
from flask import Flask, request

app = Flask(__name__)
sa
def process_video(video_path):
    # Server configuration
    server_address = ["tcp://*:5554", "tcp://*:5555"]
    worker_addresses = ["tcp://*:5556", "tcp://*:5557"]

    context = zmq.Context()

    print("Server started. Pushing jobs to workers...")

    video = cv2.VideoCapture(video_path)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    job_count = 11

    # Create the directory to store frames
    frames_dir = '/tmp/frames'
    os.makedirs(frames_dir, exist_ok=True)

    while job_count <= frame_count+10:
        # print(f"Job count: {job_count}")
        # print(f"Frame count: {frame_count+10}")

        # Get the next worker address in a cyclic manner
        worker_address = worker_addresses[job_count % len(worker_addresses)]
        server_address_push = server_address[job_count % len(worker_addresses)]

        push_socket = context.socket(zmq.PUSH)
        push_socket.bind(server_address_push)

        ret, frame = video.read()
        if not ret:
            break

        # Serialize the frame
        frame_data = cv2.imencode('.jpg', frame)[1].tobytes()

        # Convert the frame data to base64
        frame_base64 = base64.b64encode(frame_data).decode('utf-8')

        # Prepare the job data in JSON format
        job_data = {
            'frame_id': job_count,
            'image': frame_base64
        }
        job_json = json.dumps(job_data)

        # Send the job data to the worker
        push_socket.send(job_json.encode())

        print(f"Sent frame {job_count} to worker {worker_address}")

        # Create a PULL socket to receive the acknowledgment from the worker
        pull_socket = context.socket(zmq.PULL)
        pull_socket.bind(worker_address)
        ack_json = pull_socket.recv()

        # Deserialize the received acknowledgment JSON
        ack_data = json.loads(ack_json.decode())

        # Extract acknowledgment data
        frame_id = ack_data['frame_id']
        time_taken=ack_data['time_taken']
        worker_id=ack_data['worker_id']
        processed_image_base64 = ack_data['image']
        print(f"{frame_id}  processed by {worker_id} in {time_taken}")
        # Convert the processed image from base64 to NumPy array
        processed_image_data = base64.b64decode(processed_image_base64)
        processed_image_array = np.frombuffer(processed_image_data, dtype=np.uint8)

        # Decode the processed image array using OpenCV
        processed_image = cv2.imdecode(processed_image_array, cv2.IMREAD_COLOR)

        # Save the processed image
        frame_path = os.path.join(frames_dir, f"frame_{frame_id}.jpg")
        cv2.imwrite(frame_path, processed_image)
        # print(f"Saved frame {frame_id} at {frame_path}")

        job_count += 1
        if job_count >= frame_count+10:
            print("All frames processed")
            # push_socket.close()
            # context.term()
            # video.release()
            # return 

    # Close the sockets and terminate the context


@app.route('/process_video', methods=['POST'])
def process_video_route():
    if 'video' not in request.files:
        return "No video file provided", 400

    video_file = request.files['video']
    video_path = 'uploaded_video.mp4'
    video_file.save(video_path)

    # Process the video
    process_video(video_path)
    return "Video processed successfully"


if __name__ == "__main__":
    app.run(port=5000)
