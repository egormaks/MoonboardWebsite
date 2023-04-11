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

@users_bp.route('/create_user_list', methods=['POST'])
def create_user_list():
    conn = get_db()
    cur = conn.cursor()

    user_id = request.json.get('user_id')
    list_name = request.json.get('list_name')
    insert_query = """
    INSERT INTO user_lists (user_id, name)
    VALUES (%s, %s);
    """
    cur.execute(insert_query, (user_id, list_name,))
    conn.commit()

    return jsonify({'message':'created new list: ' + list_name}), 201

@users_bp.route('/get_all_user_lists', methods=['GET'])
def get_user_lists():
    conn = get_db()
    cur = conn.cursor()

    user_id = request.args.get('user_id')
    select_query = """
    SELECT *
    FROM user_lists
    WHERE user_id=%s
    """
    cur.execute(select_query, (user_id,))
    
    return jsonify(cur.fetchall())

@users_bp.route('/add_to_list', methods=['POST'])
def add_to_list():
    conn = get_db()
    cur = conn.cursor()

    list_id = request.args.get('list_id')
    route_id = request.args.get('route_id')
    insert_query = """
    INSERT INTO user_list_routes (user_list_id, moonboard_route_id)
    VALUES (%s, %s);
    """
    cur.execute(insert_query, (list_id, route_id,))
    conn.commit()

    return jsonify({'message': 'added route to list successfully.'})

@users_bp.route('/get_routes_from_list', methods=['GET'])
def get_routes_from_list():
    conn = get_db()
    cur = conn.cursor()

    user_id = request.args.get('user_id')
    list_name = request.args.get('list_name')
    select_query = """
    SELECT moonboard_routes.*
    FROM moonboard_routes
    INNER JOIN user_list_routes
        ON moonboard_routes.id = user_list_routes.moonboard_route_id
    INNER JOIN user_lists
        ON user_list_routes.user_list_id = user_lists.id
    WHERE user_lists.user_id = %s AND user_lists.name = %s;
    """
    cur.execute(select_query, (user_id, list_name,))
    
    return jsonify(cur.fetchall())
