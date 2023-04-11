import csv
from flask import Flask, jsonify, g
from flask_cors import CORS
from backend.moonboard import moonboard_bp
from backend.users import users_bp
from backend.db import get_db

app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
app.register_blueprint(moonboard_bp)
app.register_blueprint(users_bp)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



