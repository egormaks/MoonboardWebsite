from flask import current_app, request, jsonify, Blueprint, abort
from backend.db import get_db
from functools import wraps
import datetime

users_bp = Blueprint('users', __name__)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401, description='Authorization header is missing')
        
        auth_header = request.headers['Authorization']
        parts = auth_header.split(' ')
        
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            abort(401, description='Invalid Authorization header format')
        
        return f(*args, **kwargs)
    
    return decorated 

@users_bp.route('/users_get_all', methods=['GET'])
def get_all_users():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    return jsonify(users)

@users_bp.route('/users_get_curr_user_info', methods=['GET'])
def get_user_info():
    conn = get_db()
    cur = conn.cursor()

    select_query = """
    SELECT * FROM users WHERE id=%s
    """
    user_id = request.args.get('user_id')
    cur.execute(select_query, (user_id,))
    return jsonify(cur.fetchone())

@users_bp.route('/create_user', methods=['POST'])
@requires_auth
def create_user():
    auth0_id = request.json.get('auth0_id')
    email = request.json.get('email')
    name = request.json.get('name')

    conn = get_db()
    cur = conn.cursor()

    insert_query = """
    INSERT INTO users (auth0_id, email, name) VALUES (%s, %s, %s)
    """
    cur.execute(insert_query, (auth0_id, email, name,))
    conn.commit()

    return jsonify({'message': 'User created successfully'}), 201