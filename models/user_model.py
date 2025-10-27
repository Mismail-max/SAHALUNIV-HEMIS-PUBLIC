from config.db import get_connection
import bcrypt
import os

def user_exists(username, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s OR email = %s", (username, email))
    (count,) = cursor.fetchone()
    cursor.close()
    conn.close()
    return count > 0

def create_user(first_name, last_name, email, username, password):
    if user_exists(username, email):
        return False  # Prevent creation if user exists

    conn = get_connection()
    cursor = conn.cursor()
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("""
            INSERT INTO users (first_name, last_name, email, username, password_hash)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, email, username, hashed.decode('utf-8')))
        conn.commit()
        return True
    except Exception as e:
        print("Error creating user:", e)
        return False
    finally:
        cursor.close()
        conn.close()

create_user(
    first_name="System",
    last_name="Admin",
    email="info@sahal.edu.so",
    username="admin",
    password=os.getenv("DEFAULT_ADMIN_PASSWORD")
)
def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def update_password(username, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("UPDATE users SET password_hash = %s WHERE username = %s", (hashed.decode('utf-8'), username))
        conn.commit()
        return True
    except Exception as e:
        print("Error updating password:", e)
        return False
    finally:
        cursor.close()
        conn.close()
