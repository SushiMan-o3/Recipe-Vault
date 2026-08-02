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

            CREATE TABLE IF NOT EXISTS AdditionalUserInfo (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                birthday DATE,
                gender VARCHAR(10),
                profile_picture_url TEXT,
                bio TEXT
            );

            CREATE TABLE IF NOT EXISTS Recipes (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                instructions TEXT NOT NULL,
                durationInMinutes INTEGER NOT NULL,
                serving INTEGER NOT NULL,
                notes TEXT
            );

            CREATE TABLE IF NOT EXISTS ingredients (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                recipeid INTEGER NOT NULL,
                FOREIGN KEY (recipeid) REFERENCES recipes(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS equipments (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                recipeid INTEGER NOT NULL,
                FOREIGN KEY (recipeid) REFERENCES recipes(id) ON DELETE CASCADE
            );

        """)
        conn.commit()
        close_connection(conn, cursor)
    except Exception as e:
        raise Exception("Database initialization failed") from e
    
    
