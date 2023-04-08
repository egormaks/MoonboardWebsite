import psycopg2
from flask import g

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="mysecretpassword",
            host="localhost",
            port=5433
        )
    return db
