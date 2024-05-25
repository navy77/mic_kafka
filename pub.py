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

def publish_messages_data(topic_num,delay_time,msg_num,pub_loop,init):
    message_data={}

    for i in range(init,pub_loop+init):
        for j in range(1, topic_num+1):  
            topic = f"{data_topic}{j}"
            for k in range(1,msg_num+1):
                key = f"data{k}"
                message_data[key] = i
                # message_data[key] = random.randint(10000,50000)
            client.publish(topic, json.dumps(message_data))
        time.sleep(delay_time)  

def publish_messages_status(topic_num,delay_time,pub_loop,init):
    message_status={}
    for i in range(init,pub_loop+init):
        for j in range(1, topic_num+1):  
            topic = f"{status_topic}{j}"
            key = f"status"
            message_status[key]=f"{i}"
            client.publish(topic, json.dumps(message_status))
        time.sleep(delay_time) 


def publish_messages_alarm(topic_num,delay_time,pub_loop,init):
    message_alarm={}
    for i in range(init,pub_loop+init):
        for j in range(1, topic_num+1):  
            topic = f"{alarm_topic}{j}"
            key = f"status"
            message_alarm[key]=f"{i}"
            client.publish(topic, json.dumps(message_alarm))
        time.sleep(delay_time) 

if __name__ == "__main__":
    try:
        # publish_messages_data(50,0.5,10,2,51)
        publish_messages_status(50,0.5,2,1)
        # publish_messages_alarm(80,0.5,2,21)
    finally:
        client.disconnect()
        print("Disconnected from MQTT broker.")