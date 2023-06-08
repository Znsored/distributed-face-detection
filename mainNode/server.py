import json
import base64
from confluent_kafka import Producer
import os
from flask import Flask, render_template, request
import time
import psycopg2
import cv2
import uuid
from flask import Flask, request
from dotenv import dotenv_values
import random
from constructvideo import construct_vid
from storeResponse import start_consuming
from databaseOperations import get_statistics



# Create a Flask app
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './mainNode/templates'

# Connect to the PostgreSQL database
conn = psycopg2.connect("dbname=frames_get user=postgres password=root")

# Create a cursor
cursor = conn.cursor()

    # Server configuration
string_template = "{ip}:{port}"
env_vars = dotenv_values('mainNode/.env')


ip = "10.0.0.22"
port = "9093"
bootstrap_servers = string_template.format(ip=ip, port=port)

# Create producer configuration
producer_config = {
    'bootstrap.servers': bootstrap_servers,
    'client.id': 'fresh_frame_producer'
}

# Create the Kafka producer instance

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
def send_kafka(task_id):
    topic = 'request'

    #select_query = ""
    cursor.execute("SELECT image FROM save_frames WHERE task_id = (%s)",(task_id,))
    result = cursor.fetchall()
    count = 0

    for image in result:
        image=bytes(image[0])
        count = count+1
        job_count = count
        # Convert the frame data to base64
        frame_base64 = base64.b64encode(image).decode('utf-8')
        # Prepare the job data in JSON format
        job_data = {
                'task_id' : task_id,
                'frame_id': job_count,
                'image': frame_base64
            }
        job_json = json.dumps(job_data)

        # prepare messages to be sent to worker
        producer.produce(topic, value=job_json.encode('utf-8'))
        producer.flush()
    start_consuming()
    

def store_frame(task_id, frame_id, frame_data):
    # Insert the frame into the table with the provided frame_id
    cursor.execute("INSERT INTO save_frames (task_id, frame_id, image) VALUES (%s, %s, %s)", (task_id,frame_id, frame_data))






@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", result={})
    else:
        # if 'video' not in request.files:
        #     return "No video file provided", 400

        video_file = request.files['video']
        # video_path = 'uploaded_video.mp4'
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        video_file_path=os.path.join(app.config['UPLOAD_FOLDER'],'uploaded_video.mp4'.replace("\\", "/"))
        video_file.save(video_file_path)

        # Process the video
        vidcap = cv2.VideoCapture(video_file_path)
        success, frame = vidcap.read()
        frame_count = 0
        # task_id = random.randint(0, 1000)
        task_id=uuid.uuid4()
        task_id=str(task_id)
        # Initial frame_id
        frame_id = 1

        while success:
        # Convert the frame to bytes
            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = buffer.tobytes()

            # Store the frame in the database with the current frame_id
            store_frame(task_id, frame_id, frame_data)

            # Read the next frame
            success, frame = vidcap.read()
            frame_count += 1

            # Increment the frame_id
            frame_id += 1

        # Commit the transaction
        conn.commit()

        # Close the video capture, cursor, and connection
        vidcap.release()
        send_kafka(task_id)
        cursor.close()
        conn.close()
        output_file='./video.mp4'
        #upload_path = os.path.join('static', output_file)
        # path={'upload_path':'workerNode\\video.mp4'}  # Path to your video file
        stats = get_statistics(task_id)
        return render_template("showvid.html", upload_path=output_file,stats=stats)
        

        


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



