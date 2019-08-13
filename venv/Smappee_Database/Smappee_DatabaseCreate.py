# Smappee_DatabaseCreate.py
import sqlite3
'''Script to create a new SQLite database + create new data&weather table in it'''

# Create and connect to new database with chosen name
database = 'Smappee_data.db'
    #Make sure this is the same in Smappee_ConnectStore_...py and Smappee_DatabaseStore.py
conn = sqlite3.connect(database)

# Create new tables with correct scheme
c = conn.cursor()
c.execute('''CREATE TABLE data1s (utc text, publishIndex integer, CT text, device text,
            current real, phase integer, power real)''')
c.execute('''CREATE TABLE power1s (utc text, totalPower real, totalReactivePower real)''')
c.execute('''CREATE TABLE data5m (utc text, publishIndex integer, CT text, device text, commodity text,
            measurementKind text, unit text, phase text, channel integer, mRID text, value real)''')
c.execute('''CREATE TABLE weather (utc text, actualUtc text, clouds real, rain text, wind text,
            humidity real, pressure real, temperature real, uvindex real, 
            status text, detailedStatus text, weatherCode integer)''')
conn.commit()
conn.close()

