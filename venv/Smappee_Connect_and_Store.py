#Smappee_Connect_and_Store.py
import paho.mqtt.client as mqtt
import sqlite3
import time
import json
from Weather_Functions import current_weather
'''Script for subscribing to Smappee Infinity aggregated topic via MQTT
and storing the messages in a SQLite database'''
    # More info on SQLite and MQTT see SQLite_Database.py and Smappee_BasicConnect.py


'''Store json messages (in Smappee format) to a database'''
# Remark: first use Smappee_DatabaseCreate to create a new database + table

# On the aggregated topic, only a 'publishIndex' is given, but not the name of the CT/device being measured
# Therefore, a mapping is required between indexe and CT/device:
    # E.g.: publishIndex = 0 --> meter 550001259/D --> GridL1
CT_list = ['1259/D', '1259/C', '1259/B', '1259/A', '1258/D', '1258/C', '1258/B', '1258/A',
               '1260/D', '554/C', '555/B', '555/A', '554/D', '554/B', '554/A', '555/D', '555/C'
               '','','','General']
device_list = ['GridL1', 'GridL2', 'GridL3', 'NIBEL1', 'NIBEL2', 'NIBEL3', 'StoveL1', 'StoveL2',
                'StoveL3', 'Dishwasher', 'Solar8x230', 'Solar22x230', 'Oven', 'KitchenOther','WashingMachine', 'ClothesDryer', 'Poolhouse',
               '','','','General']

# Function storing data in Smappee JSON format in a database
def store_to_database(data):
    # Input JSON format: see example SmappeeJSON_Example.json
    conn = sqlite3.connect('example.db')           # Open database (same name as in Smappee_DatabaseCreate.py)
    c = conn.cursor()
    for sensor in data['intervalDatas']:
        try:                                        # Deal with last part of the data (see example json), which has no publishIndex
            publish_index = sensor['publishIndex']
        except:
            publish_index = len(device_list) - 1    # Last element on the device list is the 'general element'
        CT = CT_list[publish_index]
        device = device_list[publish_index]
        utcEndtime = sensor['utcEndtime']
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
    new_weather_entry = current_weather(utcEndtime)
    c.execute("INSERT INTO weather VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", new_weather_entry)  # Add to weather Database
    conn.commit()
    conn.close()                                    #Not sure if we need to connect and close everytime


'''Setup connection with Smappee Infinity via MQTT protocol'''
# Define server and topic to subscribe to

MQTT_SERVER = '192.168.68.109'                                                  # IP adress of Smappee Infinity
    # See word file 'CB Smappee Documentation'
MQTT_PATH = 'servicelocation/59e6a8c4-f665-4c34-a3ee-2c492da1c2de/aggregated'   # Topic: aggr. 5 min data

# Define callbacks to execute on connect and on execute

def on_connect(client, userdata, flags, rc):            # Automatically subscribe to topic on connection
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):                  # Store to database on message
    print('New data received')
    new_data = json.loads(str(msg.payload))
    print(new_data)
    store_to_database(new_data)

client = mqtt.Client()                                  # Create a new Client object
client.on_connect = on_connect                          # Use defined callback
client.on_message = on_message                          # Use defined callback
client.connect(MQTT_SERVER)                             # Connect to Smappee Infinity broker
client.loop_forever()                                   # Loop forever









