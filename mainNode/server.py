import json
import base64
from confluent_kafka import Producer
from storeResponse import start_consuming
import time
import psycopg2
import cv2
from flask import Flask, request

# Create a Flask app
app = Flask(_name_)

# Connect to the PostgreSQL database
conn = psycopg2.connect("dbname=frames_get user=postgres password=root")

# Create a cursor
cursor = conn.cursor()

    # Server configuration
bootstrap_servers = '10.0.0.22:9093'

# Create producer configuration
producer_config = {
    'bootstrap.servers': bootstrap_servers,
    'client.id': 'my_producer'
}

# # Create the Kafka producer instance

producer = Producer(producer_config)

conn = psycopg2.connect(
    database="frames_get",
    user="postgres",
    password="root",
    host="localhost",
    port="5432",
)
cursor = conn.cursor()
# Kafka topic to produce to
def send_kafka():
    topic = 'request'

    select_query = "SELECT img FROM init_frames"
    cursor.execute(select_query)
    result = cursor.fetchall()
    count = 0

    for image in result:
        count = count+1
        job_count = count
        # Convert the frame data to base64
        frame_base64 = base64.b64encode(image).decode('utf-8')
        # Prepare the job data in JSON format
        job_data = {
                'frame_id': job_count,
                'image': frame_base64
            }
        job_json = json.dumps(job_data)

        # prepare messages to be sent to worker
        producer.produce(topic, value=job_json.encode('utf-8'))
        
    producer.flush()
    start_consuming()

def store_frame(frame_id, frame_data):
    # Insert the frame into the table with the provided frame_id
    cursor.execute("INSERT INTO init_frames (frame_id, image) VALUES (%s, %s)", (frame_id, frame_data))

@app.route('/process_video', methods=['POST'])
def process_video_route():
    if 'video' not in request.files:
        return "No video file provided", 400

    video_file = request.files['video']
    video_path = 'uploaded_video.mp4'
    video_file.save(video_path)

    # Process the video
    vidcap = cv2.VideoCapture(video_path)
    success, frame = vidcap.read()
    frame_count = 0

    # Initial frame_id
    frame_id = 1

    while success:
        # Convert the frame to bytes
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()

        # Store the frame in the database with the current frame_id
        store_frame(frame_id, frame_data)

        # Read the next frame
        success, frame = vidcap.read()
        frame_count += 1

        # Increment the frame_id
        frame_id += 1

    # Commit the transaction
    conn.commit()

    # Close the video capture, cursor, and connection
    vidcap.release()
    cursor.close()
    conn.close()
    send_kafka()
    return f"Video processed successfully. {frame_count} frames stored in the database."


if _name_ == "_main_":
    app.run(port=5000)