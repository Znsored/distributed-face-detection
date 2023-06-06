from confluent_kafka.admin import AdminClient, NewTopic

def create_topic(topic_name, num_partitions, replication_factor):
    # Set up the AdminClient configuration
    admin_config = {
        'bootstrap.servers': '10.0.0.22:9093'  # Replace with your Kafka bootstrap servers
    }
    
    # Create an instance of the AdminClient
    admin_client = AdminClient(admin_config)
    
    # Create the NewTopic object with the desired topic configuration
    topic = NewTopic(
        topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor
    )
    
    # Create the topic using the AdminClient
    admin_client.create_topics([topic])
    
    # Close the AdminClient
    admin_client.close()

# Example usage to create two topics with different partitions
create_topic("request", 2, 1)  # Create "topic1" with 2 partitions and replication factor 1
create_topic("response", 1, 1)  # Create "topic2" with 4 partitions and replication factor 1
