import csv
import re
import psycopg2

# Connect to the database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="mysecretpassword",
    host="localhost",
    port="5432"
)


cur = conn.cursor()
query = """
SELECT * FROM moonboard_routes LIMIT 10;
"""

cur.execute(query)
rows = cur.fetchall()
for row in rows:
    print(row)
		
query = """
SELECT count(*) FROM moonboard_routes;
"""
cur.execute(query)
print("\n\n" + str(cur.fetchone()[0]) + " total rows in the moonboard_routes table.")
cur.close()
conn.close()
