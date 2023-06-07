from confluent_kafka.admin import AdminClient, NewTopic, Consumer
from dotenv import dotenv_values

    # Server configuration
string_template = "{ip}:{port}"
env_vars = dotenv_values('.env')


ip = env_vars["IP"]
port = env_vars["PORT"]
bootstrap_servers = string_template.format(ip=ip, port=port)


def create_topic(topic_name, num_partitions, replication_factor):
    # Set up the AdminClient configuration
    admin_config = {
        'bootstrap.servers': bootstrap_servers# Replace with your Kafka bootstrap servers
    }
    
    # Create an instance of the AdminClient
    admin_client = AdminClient(admin_config)
    
    # Create the NewTopic object with the desired topic configuration
    topic = NewTopic(
        topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor
    )
    consummer_config = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'check_topics'
    }
    consumer = Consumer(consummer_config)
    
    
    # Create the topic using the AdminClient
    admin_client.create_topics(topic)

    #list all topics
    consumer.list_topics().topics


# Example usage to create two topics with different partitions
create_topic("request", 2, 1)  # Create "topic1" with 2 partitions and replication factor 1
create_topic("response", 1, 1)  # Create "topic2" with 4 partitions and replication factor 1


consummer_config = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'check_topics'
}
consumer = Consumer(consummer_config)
consumer.list_topics().topics