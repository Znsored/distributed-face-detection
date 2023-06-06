import json
import base64
from confluent_kafka import Producer

    # Server configuration

def sendResponse(job_json):
    bootstrap_servers = '10.0.0.22:9093'

# Create producer configuration
    producer_config = {
      'bootstrap.servers': bootstrap_servers,
      'client.id': 'processed_frame_producer',
      'max.message.bytes': 1000000
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