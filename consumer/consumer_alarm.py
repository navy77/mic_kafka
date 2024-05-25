import pandas as pd
from confluent_kafka import Consumer, OFFSET_END

# Kafka configuration
kafka_conf = {
    'bootstrap.servers': 'localhost:29092,localhost:29093,localhost:29094',
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest',  # Start from the earliest message
    'enable.auto.commit': False  # Disable auto-commit
}

topics = ['topic_data']

# List of data fields for different topics
topic_fields = {
    'topic_data': ['data1', 'data2', 'data3', 'data4', 'data5', 'data6', 'data7', 'data8', 'data9', 'data10'],
}

# Create a Kafka consumer instance
consumer = Consumer(kafka_conf)
consumer.subscribe(topics)

# Function to parse the MQTT message
def parse_message(message, topic):
    parts = message.split()
    meta, values, timestamp = parts[0], parts[1], parts[2]
    meta_parts = meta.split(',')
    host = meta_parts[1].split('=')[1]
    kafka_topic = meta_parts[2].split('=')[1]
    msg_topic = meta_parts[3].split('=')[1]
    
    fields = topic_fields[topic]
    values_dict = {k: None for k in fields}
    for kv in values.split(','):
        key, value = kv.split('=')
        if key in values_dict:
            values_dict[key] = value

    return {
        'host': host,
        'kafka_topic': kafka_topic,
        'topic': msg_topic,
        'timestamp': int(timestamp),
        **values_dict
    }

# Function to handle the consumption of messages
def consume_messages():
    data = {topic: [] for topic in topics}
    try:
        while True:
            msg = consumer.poll(1.0)  # Poll with a timeout of 1 second

            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            message = msg.value().decode('utf-8')  # Assuming message is in UTF-8
            topic = msg.topic()
            parsed_data = parse_message(message, topic)
            data[topic].append(parsed_data)

            # Print messages every 50 messages per topic
            if len(data[topic]) % 50 == 0:
                if topic == 'topic_data':
                    df_data = pd.DataFrame(data[topic])
                    df_data.sort_values(by='timestamp', inplace=True)
                    print("Data from topic_data:")
                    print(df_data)
                    data[topic] = []  # Reset the list after printing
                elif topic == 'topic_status':
                    df_status = pd.DataFrame(data[topic])
                    df_status.sort_values(by='timestamp', inplace=True)
                    print("Data from topic_status:")
                    print(df_status)
                    data[topic] = []  # Reset the list after printing
                elif topic == 'topic_alarm':
                    df_alarm = pd.DataFrame(data[topic])
                    df_alarm.sort_values(by='timestamp', inplace=True)
                    print("Data from topic_alarm:")
                    print(df_alarm)
                    data[topic] = []  # Reset the list after printing

            # Manually commit the message offset
            consumer.commit(asynchronous=False)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages()
