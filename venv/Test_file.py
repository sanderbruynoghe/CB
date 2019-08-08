# Smappee_BasicConnect.py
'''File to show how to connect to Smappee infinity device via MQTT protocol (on Raspberry Pi)
+ Overview of different topics to subscribe to'''

# Python packages
    # pip or pip3 install paho-mqtt on Raspberry Pi
import paho.mqtt.client as mqtt #Python package for using the MQTT protocol
import json
import time
import sqlite3
import queue
import threading
from Smappee_DatabaseStore import store_to_database
q  = queue.Queue()
'''Server (broker) and topic data'''
MQTT_SERVER = '192.168.68.109'              # IP adress of host (broker): here: IP address of Smappee Infinity
MQTT_PATH = 'servicelocation/+/realtime'  # Topic to subscribe to
    # '+' is a wildcard and stands for every possible value
    # The + replaces the unknown uuid (see manual)
        # After testing, we can see that uuid = 59e6a8c4-f665-4c34-a3ee-2c492da1c2de, so we can replace the +
MQTT_PATH = 'servicelocation/59e6a8c4-f665-4c34-a3ee-2c492da1c2de/aggregated'
    # Other possible topics to subscribe to are given in the manual

'''Setting up a connection'''
client = mqtt.Client('2')              # Create a Client object, with a unique id (here: 'Sander')

'''def store_to_database(q):
# Input JSON format: see example SmappeeJSON_Example.json
    data = q.get()
    print(data)
    print('Go Go')
    conn = sqlite3.connect('example.db')           # Open database (same name as in Smappee_DatabaseCreate.py)
    c = conn.cursor()
    for sensor in data['intervalDatas']:
        #try:                                        # Deal with last part of the data (see example json), which has no publishIndex
        publish_index = sensor['publishIndex']
        #except:
        #    publish_index = len(device_list) - 1    # Last element on the device list is the 'general element'
        CT = CT_list[publish_index]
        device = device_list[publish_index]
        utcEndtime = sensor['utcEndtime']
        print('Tot hier')
        print('Starting for loop')
        for meas in sensor['measurements']:
            type = meas['type']
            commodity = type['commodity']
            measurementKind = type['measurementKind']
            unit = type['unit']
            phase = type['phase']
            channel = type['channel']
            mRID = type['mRID']

            value = meas['value']/1000              # Seems like measured values are 1000 times too high
            # Store measurements
            new_entry = (utcEndtime, publish_index, CT, device, commodity,
                         measurementKind, unit, phase, channel, mRID, value)
            c.execute("INSERT INTO data VALUES (?,?,?,?,?,?,?,?,?,?,?)",new_entry) #Add to measurements Database
                # Assumes that the database already exists
    # Store current weather
    #new_weather_entry = current_weather(utcEndtime)
    #c.execute("INSERT INTO weather VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", new_weather_entry)  # Add to weather Database
    conn.commit()
    print('Done')
    conn.close()                                    #Not sure if we need to connect and close everytime'''

#Define 2 functions:
    # The callback for when the client receives a CONNACK response from the server (= when connection is made)
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then all subscriptions below will autom. be renewed:
    client.subscribe(MQTT_PATH)  # Subscribe to the topic automatically, also if you reconnect for some reason
    print('Subscribed')
    # The callback for when a PUBLISH message is received from the server (actions to do when new data comes in)
def on_message(client, userdata, msg):
    print(str(msg.payload))
    q.put(json.loads(str(msg.payload)[2:]))
    print('In queue')
    store_to_database(q.get())
    print('Stored')
client.on_connect = on_connect
client.on_message = on_message

'''Connect to broker and determine when connection should be established'''
client.connect(MQTT_SERVER)  # Connect to Smappee Infinity via IP address in local network (broker)
client.loop_forever()
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





