import psycopg2
import psycopg2.extras

from config import DATABASE_URL


def create_connection():
    conn, cursor = None, None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    except Exception as e:
        raise Exception("Database connection failed") from e

    return conn, cursor

def close_connection(conn, cursor):
    try:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    except Exception as e:
        raise Exception("Failed to close database connection") from e


def init_db():
    try:
        conn, cursor = create_connection()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                username VARCHAR(20) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            );
        """)
        conn.commit()
        close_connection(conn, cursor)
    except Exception as e:
        raise Exception("Database initialization failed") from e
    
    
