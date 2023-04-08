from flask import current_app, request, jsonify, Blueprint
from backend.db import get_db

moonboard_bp = Blueprint('moonboard', __name__)

@moonboard_bp.route('/moonboard_get_all', methods=['GET'])
def get_all_moonboard_routes():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM moonboard_routes")
    routes = cur.fetchall()
    return jsonify(routes)

@moonboard_bp.route('/moonboard_get_top_n', methods=['GET'])
def get_n_moonboard_routes():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM moonboard_routes LIMIT %s', (int(request.args.get('N')),))
    routes = cur.fetchall()
    return jsonify(routes)
