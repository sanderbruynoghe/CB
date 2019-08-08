# Smappee DatabaseStore.py
import json
import sqlite3
from Weather_Functions import current_weather

# On the aggregated topic, only a 'publishIndex' is given, but not the name of the CT/device being measured
# Therefore, a mapping is required between indexe and CT/device:
    # E.g.: publishIndex = 0 --> meter 550001259/D --> GridL1
CT_list = ['1259/D', '1259/C', '1259/B', '1259/A', '1258/D', '1258/C', '1258/B', '1258/A',
               '1260/D', '554/C', '555/B', '555/A', '554/D', '554/B', '554/A', '555/D', '555/C',
               '','','','General']
device_list = ['GridL1', 'GridL2', 'GridL3', 'NIBEL1', 'NIBEL2', 'NIBEL3', 'StoveL1', 'StoveL2',
                'StoveL3', 'Dishwasher', 'Solar8x230', 'Solar22x230', 'Oven', 'KitchenOther','WashingMachine', 'ClothesDryer', 'Poolhouse',
               '','','','General']

def store_to_database(data):
    # Input JSON format: see example SmappeeJSON_Example.json
    conn = sqlite3.connect('Smappee_data.db')           # Open database (same name as in Smappee_DatabaseCreate.py)
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
            c.execute("INSERT INTO data VALUES (?,?,?,?,?,?,?,?,?,?,?)",new_entry)          # Add to measurements Database
                # Assumes that the database already exists
    # Store current weather
    new_weather_entry = current_weather(utcEndtime)
    c.execute("INSERT INTO weather VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", new_weather_entry)    # Add to weather Database
        # Assumes that the database already exists
    conn.commit()
    conn.close()
    print('New data added')