import json
import base64
from confluent_kafka import Producer
from storeResponse import start_consuming
from dotenv import dotenv_values
import time

    # Server configuration
string_template = "{ip}:{port}"
env_vars = dotenv_values('mainNode/.env')


ip = env_vars["IP"]
port = env_vars["PORT"]
bootstrap_servers = string_template.format(ip=ip, port=port)

# Create producer configuration
producer_config = {
    'bootstrap.servers': bootstrap_servers,
    'client.id': 'fresh_frame_producer'
}

# Create the Kafka producer instance

producer = Producer(producer_config)

# Kafka topic to produce to
topic = 'request'

path = r'C:\\Users\\athre\\Desktop\\docker\\workerNode\\mainNode\\image.jpeg'
 

with open(path,'rb') as file:
    img = file.read()
if img is None:
    print("img empty")
job_count=1

for i in range(2):

    job_count = i
    # Convert the frame data to base64
    frame_base64 = base64.b64encode(img).decode('utf-8')
    # Prepare the job data in JSON format
    job_data = {
            'frame_id': job_count,
            'image': frame_base64
        }
    job_json = json.dumps(job_data)

    # prepare messages to be sent to worker     
    producer.produce(topic, value=job_json.encode('utf-8'))

#flush messages and close connection

producer.flush()
# start_consuming()