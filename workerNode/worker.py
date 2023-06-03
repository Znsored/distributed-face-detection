from confluent_kafka import Consumer
import base64
import logging
import json
import time
from faceDetector import get_features
from dotenv import dotenv_values

logging.basicConfig(level=logging.INFO)

string_template = "{ip}:{port}"
env_vars = dotenv_values('.env')


ip = env_vars["IP"]
port = env_vars["PORT"]

logging.basicConfig(level=logging.INFO)

# Kafka broker(s) configuration
bootstrap_servers = string_template.format(ip=ip, port=port)
logging.info(bootstrap_servers)

# Create consumer configuration
consumer_config = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'my_consumer',
    'auto.offset.reset': 'earliest'
}

# Create the Kafka consumer instance
consumer = Consumer(consumer_config)

# Kafka topic to consume from
topic = 'my_topic'

# Subscribe to the Kafka topic
consumer.subscribe([topic])

# Consume messages from the Kafka topic
while True:
    logging.info("waiting for message")
    message = consumer.poll(1.0)

    if message is None:
        time.wait(3.0)
    message = consumer.poll(1.0)
    if message is None:
        time.wait(3.0)
        continue

    if message.error():
        logging.info(f"Consumer error: {message.error()}")
        continue

    # Decode the image from the message value
    json_message = message.value().decode('utf-8')
    try:
        job_data = json.loads(json_message)
    except json.JSONDecodeError as e:
        #print(f"Error decoding JSON message: {e}")
        continue
    frame_id = job_data['frame_id']
    image_base64 = job_data['image']

    # Decode the image from Base64
    image_data = base64.b64decode(image_base64)

    start_time = time.time()
    processed_image = get_features(image_data)
    #processed_image = image_data
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


        #push_socket.send(ack_json.encode())
    
    logging.info(f"Successfully Sent Image in {time_taken}")


    # Process the image data
    # ...

# Close the consumer
consumer.close()
