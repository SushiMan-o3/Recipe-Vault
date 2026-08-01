import psycopg2
import dotenv

# load database url
dotenv.load_dotenv()

def create_connection():
    conn, cursor = None, None
    
    try:
        conn = psycopg2.connect()
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
        conn, cursor = create_connection()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(20) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            );
        """)
        conn.commit()
        close_connection(conn, cursor)
    except:
        raise Exception("Database initialization failed")
    
    
