import psycopg2
from psycopg2.extras import DictCursor

def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname="wiwi",
            user="admin",
            password="ouss3110",
            host="localhost",
            port="5432"
        )
        return connection
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise
