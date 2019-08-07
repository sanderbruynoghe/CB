# Smappee_DatabaseCreate.py
import sqlite3
'''Script to create a new SQLite database + create new data&weather table in it'''

# Create and connect to new database with chosen name
database = 'example.db'             #Make sure this is the samen in Smappee_Connect_and_Store.py
conn = sqlite3.connect(database)

# Create new table with certain scheme
c = conn.cursor()
c.execute('''CREATE TABLE data (utc text, publishIndex integer, CT text, device text, commodity text,
            measurementKind text, unit text, phase text, channel integer, mRID text, value real)''')
c.execute('''CREATE TABLE weather (utc text, actualUtc text, clouds real, rain text, wind text,
            humidity real, pressure real, temperature real, uvindex real, 
            status text, detailedStatus text, weatherCode integer)''')
conn.commit()
conn.close()