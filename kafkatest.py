import time
import cv2
import numpy as np
import json
import base64
from confluent_kafka import Producer




    # Server configuration
bootstrap_servers = '10.0.0.22:9093'

# Create producer configuration
producer_config = {
    'bootstrap.servers': bootstrap_servers,
    'client.id': 'my_producer'
}

# Create the Kafka producer instance

producer = Producer(producer_config)

# Kafka topic to produce to
topic = 'my_topic'

    





path = r'F:\\img.jpg'
 
# Using cv2.imread() method
# Using 0 to read image in grayscale mode
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

for i in range(10):
        
        

    job_count = i

        # Convert the frame data to base64
    frame_base64 = base64.b64encode(img).decode('utf-8')

        # Prepare the job data in JSON format
    job_data = {
            'frame_id': job_count,
            'image': frame_base64
        }
    job_json = json.dumps(job_data)

        # Send the job data to the worker
        
    producer.produce(topic, value=job_json.encode('utf-8'))
producer.flush()


       

    # Close the sockets and terminate the context