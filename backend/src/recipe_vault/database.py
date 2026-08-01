import psycopg2
from dotenv import load_dotenv
import os

# load database url
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def create_connection():
    conn, cursor = None, None
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
    except:
        raise Exception("Database connection failed")
    
    return conn, cursor

def close_connection(conn, cursor):
    try:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    except:
        raise Exception("Failed to close database connection")
    
    
def init_db():
    try:
        conn, cursor = create_connection(DATABASE_URL)
        
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
    except:
        raise Exception("Database initialization failed")
    
    
