import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

''' Example execution.
cur.execute("INSERT INTO Products (ProductName, AcquiredDate, ProductCode) VALUES (?, ?, ?)",
            ('PSX', '06282024', 'PSX5501PU18062820241')
            )
'''

connection.commit()
connection.close()
print("Database Successfully initialized.")
