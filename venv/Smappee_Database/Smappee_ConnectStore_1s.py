# Smappee_ConnectStore.py
'''Script storing Smappee 1s data'''
import paho.mqtt.client as mqtt
import json
import sqlite3
import Smappee_DatabaseStore

'''Server (broker) and topic data'''
MQTT_SERVER = '192.168.68.109'                                                  # Smappee Infinity IP address
MQTT_PATH = 'servicelocation/59e6a8c4-f665-4c34-a3ee-2c492da1c2de/realtime'   # Aggregated 5 min data
client = mqtt.Client()

    # The callback for when the client receives a CONNACK response from the server (= when connection is made)
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_PATH)
    print('Subscribed to', MQTT_PATH)

    # The callback for when a PUBLISH message is received from the server (actions to do when new data comes in)
def on_message(client, userdata, msg):
    new_data = json.loads(msg.payload.decode('utf8'))
    print('Started storing')
    Smappee_DatabaseStore.store_to_database_1s(new_data)                        # Use 1s storing function

client.on_connect = on_connect
client.on_message = on_message

'''Connect to broker and loop forever'''
client.connect(MQTT_SERVER)
client.loop_forever()
















