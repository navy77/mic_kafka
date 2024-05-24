from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata
import pandas as pd

# Setup Kafka Consumer
consumer = KafkaConsumer(
    'telegraf',
    bootstrap_servers=['localhost:9093'],
    auto_offset_reset='earliest',
    group_id='my-consumer-group',
    enable_auto_commit=False
)

def parse_msg(line):
    parts = line.strip().split(' ')
    measurement_tags, fields, timestamp = parts[0], parts[1], parts[2]

    measurement, *tag_parts = measurement_tags.split(',')
    tags = {}
    for tag in tag_parts:
        key, value = tag.split('=')
        tags[key] = value
    field_data = {}
    for field in fields.split(','):
        key, value = field.split('=')
        field_data[key] = float(value)

    return measurement, tags, field_data, timestamp

def process_data(data_batch):
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data_batch)
    print(df)
    # You can add more processing logic here, like saving to a database, etc.
    return df

data = []

try:
    print("Starting the consumer")
    for message in consumer:
        msg = message.value.decode('utf-8')
        print("Received message:", msg)
        
        # Parse message and prepare data for DataFrame
        measurement, tags, fields, timestamp = parse_msg(msg)
        entry = {**tags, **fields, "timestamp": timestamp, "measurement": measurement}
        data.append(entry)

        # Process in batches of 10
        if len(data) >= 3:
            df = process_data(data)
            data = []  # Reset batch data list after processing
            # After processing the batch, commit the offsets
            tp = TopicPartition(message.topic, message.partition)
            offsets = {tp: OffsetAndMetadata(message.offset + 1, None)}
            consumer.commit(offsets=offsets)

except KeyboardInterrupt:
    print("Stopping consumer")
    if data:
        # Process the remaining data if the program is interrupted
        df = process_data(data)
        data = []
        tp = TopicPartition(message.topic, message.partition)
        offsets = {tp: OffsetAndMetadata(message.offset + 1, None)}
        consumer.commit(offsets=offsets)
finally:
    consumer.close()  # Clean up and close the connection when done or interrupted