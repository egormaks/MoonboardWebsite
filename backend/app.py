import csv
import psycopg2
from flask import Flask, jsonify, request, g

app = Flask(__name__)

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

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    
@app.route('/moonboard_get_all', methods=['GET'])
def get_all_moonboard_routes():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM moonboard_routes")
    routes = cur.fetchall()
    return jsonify(routes)

@app.route('/moonboard_get_top_n', methods=['GET'])
def get_n_moonboard_routes():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM moonboard_routes LIMIT %s', (int(request.args.get('N')),))
    routes = cur.fetchall()
    return jsonify(routes)

