from kafka import KafkaConsumer
import psycopg2
import json
import time


# Constants
KAFKA_BROKER_URL = 'broker:9092'
KAFKA_TOPIC = 'kafka-topic-postgress'
KAFKA_CONSUMER_ID = 'consumer'

POSTGRES_HOST = 'postgres'
POSTGRES_DB = 'postgres'
POSTGRES_USER = 'postgres_user'
POSTGRES_PASSWORD = 'secret'


# Deserializer
def deserializer(value):
    if value is None:
        return
    
    try:
        return json.loads(value.decode('utf-8'))
    except:
        print('Unable to decode')
        return None
    

# Kafka Consumer
consumer = None
conn = None
max_retries = 10
retry_delay = 5

for i in range(max_retries):
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_BROKER_URL],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=KAFKA_CONSUMER_ID,
            value_deserializer=deserializer
        )
        print(f'Attempt {i+1}: Kafka Consumer initialized successfully!')
        break
    except Exception as e:
        print(f'Attempt {i+1}: Errror intializing consumer: {e}. Retrying in {retry_delay} seconds...')
        time.sleep(retry_delay)


# Postgres
for i in range(max_retries):
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST, 
            database=POSTGRES_DB,
            user=POSTGRES_USER, 
            password=POSTGRES_PASSWORD
        )
        print(f"Attempt {i+1}: Postgres is connected successfully")
        break
    except Exception as e:
        print(e)
        time.sleep(retry_delay)


if conn is not None:
    print('Connection established to PostgreSQL.')
    cur = conn.cursor()
else:
    print('Connection NOT established to PostgreSQL.')


# Connect PostgreSQL to Kafka
def kafka_consumer(conn=conn):
    for message in consumer:
        data = message.value
        print(data)
        cur.execute(
            "INSERT INTO telemtry_data (ts, device, co, humidity, light, lpg, motion, smoke, temp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
            (data['ts'], data['device'], data['co'], data['humidity'], data['light'], data['lpg'], data['motion'], data['smoke'], data['temp'])
        )
        conn.commit()

    conn.close()


if __name__ == "__main__":
    kafka_consumer()