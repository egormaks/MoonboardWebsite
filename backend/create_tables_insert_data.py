import csv
import re
import psycopg2

def create_table(cur, table_name, schema):
    cur.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')")
    table_exists = cur.fetchone()[0]
    if table_exists:
        cur.execute(f"DROP TABLE {table_name}")
    cur.execute(schema)

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="mysecretpassword",
    host="localhost",
    port="5432"
)

user_schema = """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        auth0_id text UNIQUE NOT NULL,
        email text NOT NULL,
        name text NOT NULL
    );
"""

moonboard_routes_schema = """
    CREATE TABLE moonboard_routes (
        id SERIAL PRIMARY KEY,
        name TEXT,
        grade TEXT,
        board_angle INTEGER,
        moonboard_year INTEGER,
        setter TEXT,
        start_holds TEXT[],
        middle_holds TEXT[],
        end_holds TEXT[],
        rules TEXT,
        is_benchmark BOOLEAN
    );
"""

user_completed_problems_schema = """
    CREATE TABLE user_completed_problems (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        route_id INTEGER REFERENCES moonboard_routes(id),
        completed_on TIMESTAMP,
        video_url VARCHAR,
        user_grade TEXT
    );
"""

user_lists_schema = """
    CREATE TABLE user_lists (
        id SERIAL PRIMARY KEY,
        user_id integer REFERENCES users(id),
        name text
    );
"""

user_list_routes_schema = """
    CREATE TABLE user_list_routes (
        user_list_id integer REFERENCES user_lists(id),
        moonboard_route_id integer REFERENCES moonboard_routes(id),
        PRIMARY KEY (user_list_id, moonboard_route_id)
    );
"""

cur = conn.cursor()
actual_lines = 0
added_lines = 0
with open('mb_problems.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    for line in reader:
        actual_lines += 1
        try:
            line[2] = int(line[2])
            line[3] = int(line[3])
            line[5] = [x for x in line[5].split(",") if x]
            line[6] = [x for x in line[6].split(",") if x]
            line[7] = [x for x in line[7].split(",") if x]
            cur.execute("""
    			INSERT INTO moonboard_routes (id, grade, board_angle, moonboard_year, setter, start_holds, middle_holds, end_holds, rules, is_benchmark)
    			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
				""", line)
            added_lines += 1
        except ValueError:
            continue
    conn.commit()

print(str(actual_lines) + ": actual lines")
print(str(added_lines) + ": lines that were added")
cur.close()
conn.close()
