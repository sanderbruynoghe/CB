# SQLite_Database.py
import sqlite3

# Step 1: create 'connection object' representing the database:
conn = sqlite3.connect('example.db')        #Do the same for accessing the database later on

# Step 2: create Cursor object to be able to perform SQL commands on the database:
c = conn.cursor()

# Step 3: adding data to the database:
    # Create table
#c.execute('''CREATE TABLE stocks
#             (date text, trans text, symbol text, qty real, price real)''')
    # Insert a row of data
#c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    # Always have to save (commit) the changes
#conn.commit()

# Step 4: querying the database:
    # Put the query in an execute statement
    # fetchall() returns a list [] of tuples (rows)
a = c.execute("SELECT * FROM stocks WHERE symbol = 'RHAT'").fetchall()     #Use "" (double) so you can use '' (single) in query
    # To use variables from Python in the query, use ? as placeholder
    # and provide tuple as second argument to placeholder:
symbol = ('RHAT',) #Tuple with only one value here
print(c.execute('SELECT * FROM stocks WHERE symbol=?', symbol).fetchall())

# Step 5: inserting multiple rows at once: c.executemany:
purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]
#c.executemany("INSERT INTO stocks VALUES (?,?,?,?,?)", purchases) #Executemany takes list of tuples as second argument
#conn.commit()      #Don't forget commit!
try:  # Deal with last part of the data: general data without publishIndex
    publish_index = sensor['publishIndex']
except:
    publish_index = 17  # Last element on the device list is the 'general element'
# Step 5: close the connection (changes are lost if not commited before closing)
#conn.close()