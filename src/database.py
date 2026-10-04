import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'calculator.db')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS calculation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expression TEXT NOT NULL,
            result REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def save_history(expression, result):
    conn = get_connection()
    cursor = conn.execute(
        'INSERT INTO calculation_history (expression, result) VALUES (?, ?)',
        (expression, result)
    )
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id


def get_all_history():
    conn = get_connection()
    rows = conn.execute(
        'SELECT id, expression, result, created_at '
        'FROM calculation_history ORDER BY id DESC'
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_history(record_id):
    conn = get_connection()
    cursor = conn.execute(
        'DELETE FROM calculation_history WHERE id = ?', (record_id,)
    )
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted