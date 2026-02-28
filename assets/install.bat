import sqlite3

from config import DATABASE_NAME
DB_NAME = DATABASE_NAME

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY
        )
    """)

    conn.commit()
    conn.close()


def add_user(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))

    conn.commit()
    conn.close()


def get_users_count():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    conn.close()
    return count


def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users")
    users = [row[0] for row in cursor.fetchall()]

    conn.close()
    return users