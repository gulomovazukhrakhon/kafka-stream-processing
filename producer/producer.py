# Import Libraries
import time
import json
import pandas as pd
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError


# Constants
FILE_PATH = "./dataset/iot_telemetry_data.csv"
KAFKA_BROKER_URL = 'broker:9092'
KAFKA_TOPIC = 'kafka-topic-postgress'
KAFKA_ANDMIN_CLIENT = 'admin-client'
PRODUCER_CLIENT_ID = 'producer'


## Lifespan
def create_topic_if_not_exists():
    admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_BROKER_URL,
        client_id=KAFKA_ANDMIN_CLIENT
    )

    if KAFKA_TOPIC not in admin_client.list_topics():
        try:
            admin_client.create_topics([
                NewTopic(
                    name=KAFKA_TOPIC,
                    num_partitions=1,
                    replication_factor=1
                )
            ]
        )
        except TopicAlreadyExistsError as e:
            print(f"Topic {KAFKA_TOPIC} already exists! Skipping the creation...")


## Serializer
def serializer(message):
    return json.dumps(message).encode() 


## Initialize Producer
producer = None
max_retries = 10
retry_delay = 5 # seconds
for i in range(max_retries):
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER_URL,
            value_serializer=serializer,
            client_id=PRODUCER_CLIENT_ID,
        )
        print(f"Attempt {i+1}: Kafka producer initialized successfully.")
        break
    except Exception as e:
        print(f"Attempt {i+1}: Error initializing producer: {e}. Retrying in {retry_delay} seconds...")
        time.sleep(retry_delay)


## Reading row-by-row simulating real-time data
def real_time_simulation(file_path=FILE_PATH):
    df = pd.read_csv(file_path)

    for _, row in df.iterrows():
        message = row.to_dict()
        print("Sending:", message)
        try:
            producer.send(KAFKA_TOPIC, value=message)
            producer.flush()
        except Exception as e:
            print(f'Failed to send message: {e}')

        time.sleep(5)


if __name__ == "__main__":
    create_topic_if_not_exists()
    real_time_simulation()