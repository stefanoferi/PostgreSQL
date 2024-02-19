import os

# Get environment variables
USER = os.getenv('API_USER')

print('Hello world, ' + USER)
print('Hello world 2')

import psycopg2

# Connect to your postgres DB
conn = psycopg2.connect("host=db dbname=northwind user=postgres password=example")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM us_states")

# Retrieve query results
records = cur.fetchall()

for record in records:
    print(record)