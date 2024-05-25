from confluent_kafka import Consumer, KafkaException
import pandas as pd

# Define the topic fields for each topic
topic_fields = {
    'topic_data': ['data1', 'data2', 'data3', 'data4', 'data5', 'data6', 'data7', 'data8', 'data9', 'data10'],
    'topic_status': ['status'],
    'topic_alarm': ['status']
}

def create_consumer():
    conf = {
        'bootstrap.servers': 'localhost:29092,localhost:29093,localhost:29094',  # Your Kafka server config
        'group.id': "my-group",  # Consumer group ID
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False  # Manually commit offsets
    }
    consumer = Consumer(conf)
    return consumer

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

def fetch_data(consumer, topic):
    consumer.subscribe([topic])
    data = []
    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Poll with a timeout of 1 second
            if msg is None:
                break  # No more messages
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    continue  # End of partition event
                else:
                    print(f"Consumer error: {msg.error()}")
                    continue

            parsed_data = parse_message(msg.value().decode('utf-8'), topic)
            data.append(parsed_data)

            # Manually commit the message offset
            consumer.commit(message=msg)
    finally:
        consumer.close()

    return data

def create_dataframe(data):
    df = pd.DataFrame(data)
    return df

def main():
    consumer = create_consumer()
    topic = "topic_status"
    data = fetch_data(consumer, topic)
    df = create_dataframe(data)
    print(df)

if __name__ == "__main__":
    main()
