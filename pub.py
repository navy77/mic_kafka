import paho.mqtt.client as mqtt
import time
import json
import random

broker_address = "192.168.0.160" 
client = mqtt.Client(callback_api_version=2,client_id="pub1")
client.connect(broker_address)
data_topic = "data/mic/test/a"
status_topic = "status/mic/test/a"
alarm_topic = "alarm/mic/test/a"

def publish_messages_data(topic_num,delay_time,msg_num):
    message_data={}
    for i in range(1,msg_num+1):
        key = f"data{i}"
        message_data[key] = random.randint(10000,50000)

    for i in range(1, topic_num+1):  
        topic = f"{data_topic}{i}"
        client.publish(topic, json.dumps(message_data))
        time.sleep(delay_time)  

def publish_messages_status(topic_num,delay_time):
    message_status={"status":"run"}
    for i in range(1, topic_num+1):  
        topic = f"{status_topic}{i}"
        client.publish(topic, json.dumps(message_status))
        time.sleep(delay_time) 

def publish_messages_alarm(topic_num,delay_time):
    message_alarm={"status":"mc_crack"}
    for i in range(1, topic_num+1):  
        topic = f"{alarm_topic}{i}"
        client.publish(topic, json.dumps(message_alarm))
        time.sleep(delay_time) 

if __name__ == "__main__":
    try:
        publish_messages_data(100,0.1,10)
        publish_messages_status(20,1)
        publish_messages_alarm(20,1)
    finally:
        client.disconnect()
        print("Disconnected from MQTT broker.")
