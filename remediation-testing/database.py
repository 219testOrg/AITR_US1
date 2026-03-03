import sqlite3
import os

def init_db():
    os.makedirs('db', exist_ok=True)
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        is_admin BOOLEAN DEFAULT 0
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        key TEXT NOT NULL,
        value TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    cursor.execute("INSERT OR IGNORE INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)",
                  ('admin', 'admin123', 'admin@example.com', 1))
    cursor.execute("INSERT OR IGNORE INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)",
                  ('user', 'password123', 'user@example.com', 0))
    
    cursor.execute("INSERT OR IGNORE INTO user_data (user_id, key, value) VALUES (?, ?, ?)",
                  (1, 'api_key', 'sk_test_abcdefghijklmnopqrstuvwxyz12345'))
    cursor.execute("INSERT OR IGNORE INTO user_data (user_id, key, value) VALUES (?, ?, ?)",
                  (1, 'credit_card', '4111-1111-1111-1111'))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database initialized with sample data.")

def authenticate_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    conn.close()
    
    return user is not None

def get_user_data(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT u.username, ud.key, ud.value FROM users u JOIN user_data ud ON u.id = ud.user_id WHERE u.username = ?", (username,))
    data = cursor.fetchall()
    conn.close()
    
    return data

if __name__ == "__main__":
    init_db()
    print("Try to authenticate:", authenticate_user("admin", "admin123"))
    print("User data:", get_user_data("admin")) 