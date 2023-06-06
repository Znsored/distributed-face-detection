import json
import base64
from confluent_kafka import Producer
from dotenv import dotenv_values

    # Server configuration

def sendResponse(job_json):
    string_template = "{ip}:{port}"
    env_vars = dotenv_values('.env')


    ip = env_vars["IP"]
    port = env_vars["PORT"]
    bootstrap_servers = string_template.format(ip=ip, port=port)

# Create producer configuration
    producer_config = {
      'bootstrap.servers': bootstrap_servers,
      'client.id': 'processed_frame_producer'
    }

# Create the Kafka producer instance

    producer = Producer(producer_config)

# Kafka topic to produce to
    topic = 'response'
    # prepare messages to be sent to worker     
    producer.produce(topic, value=job_json.encode('utf-8'))

#flush messages and close connection
    producer.flush()
    return None