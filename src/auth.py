# auth.py
import sqlite3
import hashlib

def get_db_connection():
    try:
        return sqlite3.connect('users.db')
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def create_table():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    hashed_password = hash_password(password)
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            print("User already exists.")
        except sqlite3.Error as e:
            print(f"Error adding user: {e}")
        finally:
            conn.close()

def check_user(username, password):
    hashed_password = hash_password(password)
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result and result[0] == hashed_password:
                return True
        except sqlite3.Error as e:
            print(f"Error checking user: {e}")
        finally:
            conn.close()
    return False
