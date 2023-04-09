from flask import current_app, request, jsonify, Blueprint
from backend.db import get_db
import datetime

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

@moonboard_bp.route('/moonboard_submit_send', methods=['POST'])
def submit_sent_route():
    conn = get_db()
    cur = conn.cursor()

    user_id = request.form.get('user_id')
    route_id = request.form.get('curr_route_name') 
    current_date = datetime.date.today()
    formatted_date = current_date.strftime('%d/%m/%Y')
    user_grade = request.form.get('user_grade')
    user_notes = request.form.get('notes')
    video_blob = request.form.get('submitted_video_blob')
    video_url = process_video_blob(video_blob)

    insert_query = """
    INSERT INTO user_completed_problems (user_id, route_id, completed_on, video_url, user_grade, notes)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cur.execute(insert_query, (user_id, route_id, 
                formatted_date, video_url, user_grade, user_notes))
    conn.commit()

    return {'message': 'Insert successful', 'data':(user_id, route_id, 
                formatted_date, video_url, user_grade, user_notes)}

@moonboard_bp.route('/moonboard_get_sent_routes', methods=['GET'])
def get_sent_routes():
    conn = get_db()
    cur = conn.cursor()

    select_query = """
    SELECT *
    FROM user_completed_problems 
    WHERE user_id=%s
    """
    user_id = request.args.get('user_id')
    cur.execute(select_query, (user_id,))
    routes = cur.fetchall()
    return jsonify(routes)

@moonboard_bp.route('/moonboard_search_routes_substr', methods=['GET'])
def search_moonboard_routes():
    conn = get_db()
    cur = conn.cursor()

    search_query = """
    SELECT * FROM moonboard_routes WHERE id ILIKE %s
    """
    search_term = request.args.get("term")
    cur.execute(search_query, ('%' + search_term + '%',))
    routes = cur.fetchall()
    return jsonify(routes)

@moonboard_bp.route('/moonboard_retrieve_single_route_by_id', methods=['GET'])
def retrieve_single_route_by_id():
    conn = get_db()
    cur = conn.cursor()

    search_query = """
    SELECT * FROM moonboard_routes WHERE id=%s
    """

    route_id = request.args.get("id")
    cur.execute(search_query,(route_id,))
    route_info = cur.fetchone()
    return jsonify(route_info)


# to add more filters later
@moonboard_bp.route('/moonboard_retrieve_filtered_routes')
def retrieve_filtered_routes():
    conn = get_db()
    cur = conn.cursor()

    start_grade = str(request.args.get("start_grade", default="3"))
    end_grade = str(request.args.get("end_grade", default="8A"))
    benchmarks_only = request.args.get("benchmarks_only", default=False)
    args = (start_grade, end_grade)

    search_query = """
    SELECT * FROM moonboard_routes WHERE grade BETWEEN %s AND %s 
    """
    if (benchmarks_only):
        search_query += "AND is_benchmark=%s"
        args += (str(benchmarks_only),)

    cur.execute(search_query, args)
    routes = cur.fetchall()
    return jsonify(routes)
    

def process_video_blob(blob):
    # TODO
    return blob


