import paho.mqtt.client as mqtt
import json
import time
import sqlite3
import queue
import threading
import Smappee_DatabaseStore_test

'''Server (broker) and topic data'''
MQTT_SERVER = '192.168.68.109'
MQTT_PATH = 'servicelocation/59e6a8c4-f665-4c34-a3ee-2c492da1c2de/realtime'
client = mqtt.Client()

q = queue.Queue()

#Define 2 functions:
    # The callback for when the client receives a CONNACK response from the server (= when connection is made)
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_PATH)
    print('Subscribed')
    # The callback for when a PUBLISH message is received from the server (actions to do when new data comes in)
def on_message(client, userdata, msg):
    q.put(str(msg.payload)[2:])
    print('Message received')
    print('qsize is', q.qsize())
    Smappee_DatabaseStore_test.store_to_database(q)
    print('Message stored')
client.on_connect = on_connect
client.on_message = on_message

'''Connect to broker and determine when connection should be established'''
client.connect(MQTT_SERVER)  # Connect to Smappee Infinity via IP address in local network (broker)
# client.loop_forever()
client.loop_start()
while True:
    if q.qsize() != 0:
       data = json.loads(q.get())
       print(data)
       store_to_database(json.loads(q.get()))
       print('Processed')
       time.sleep(10)
   else:
       print('Nothing in queue')
       time.sleep(60*5)
time.sleep(10)

client.loop_stop()


'''def storing():
    while True:
        print('Busy')
        time.sleep(10)
       #if q.qsize() != 0:
       #    store_to_database(json.loads(q.get()))
       #    print('Processed')
       #    time.sleep(60*5)
       #else:
       #    print('Nothing in queue')
       #    time.sleep(60*5)
def running():
    client.loop_forever()
# Threads running
th2 = threading.Thread(target=storing()).start()
th1 = threading.Thread(target=running()).start()'''





