import csv
from flask import Flask, jsonify, g
from backend.moonboard import moonboard_bp
from backend.db import get_db

app = Flask(__name__)
app.register_blueprint(moonboard_bp)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



