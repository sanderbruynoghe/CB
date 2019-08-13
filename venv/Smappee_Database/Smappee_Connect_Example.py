# Smappee_Connect_Example.py
'''File to show how to connect to Smappee infinity device via MQTT protocol (on Raspberry Pi)
+ Overview of different topics to subscribe to'''

# Python packages
    # pip install paho-mqtt on Raspberry Pi
import paho.mqtt.client as mqtt #Python package for using the MQTT protocol
import json
import time
import queue

'''Server (broker) and topic data'''
MQTT_SERVER = '192.168.68.109'              # IP adress of host (broker): here: IP address of Smappee Infinity
MQTT_PATH = 'servicelocation/+/realtime'  # Topic to subscribe to
    # '+' is a wildcard and stands for every possible value
    # The + replaces the unknown uuid (see manual)
        # After testing, we can see that uuid = 59e6a8c4-f665-4c34-a3ee-2c492da1c2de, so we can replace the +
MQTT_PATH = 'servicelocation/59e6a8c4-f665-4c34-a3ee-2c492da1c2de/realtime'
    # Other possible topics to subscribe to are given in the manual

'''Setting up a connection'''
client = mqtt.Client()              # Create a Client object

#Define 2 functions:
    # The callback for when the client receives a CONNACK response from the server (= when connection is made)
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then all subscriptions below will autom. be renewed:
    client.subscribe(MQTT_PATH)  # Subscribe to the topic automatically, also if you reconnect for some reason

    # The callback for when a PUBLISH message is received from the server (actions to do when new data comes in)
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))       #Simply print received data
    # Add them to the Client object

client.on_connect = on_connect
client.on_message = on_message

'''Connect to broker and determine when connection should be established'''
client.connect(MQTT_SERVER)  # Connect to Smappee Infinity via IP address in local network (broker)

client.loop_forever()
# Other loop*() functions are available, see: https://pypi.org/project/paho-mqtt/#network-loop


