import json
from Smappee_DatabaseStore import store_to_database
import sqlite3


conn = sqlite3.connect('example.db')
c = conn.cursor()
print(c.execute("SELECT utc, device, value from data WHERE measurementKind LIKE 'ACTIVE_POWER'").fetchall())
#print(c.execute('SELECT * from weather').fetchall())
conn.close()
