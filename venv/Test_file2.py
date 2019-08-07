import sqlite3

conn = sqlite3.connect('example2.db')
c = conn.cursor()
for row in c.execute("SELECT * FROM data").fetchall():
     print(row)
conn.close()