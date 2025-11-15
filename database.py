import sqlite3
import os
from datetime import datetime

# Database path
DB_PATH = os.getenv('DATABASE_PATH', './data/users.db')

def init_database():
    """Initialize SQLite database with required tables"""
    
    # Create data folder if doesn't exist
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table 1: Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_interaction TIMESTAMP
        )
    ''')
    
    # Table 2: Assessment results
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            phq9_score INTEGER,
            severity TEXT,
            answers TEXT,
            assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Table 3: Conversation logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_message TEXT,
            bot_response TEXT,
            message_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully")

def save_user(user_id, username, first_name, last_name):
    """Save new user to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO users 
            (user_id, username, first_name, last_name, last_interaction)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, datetime.now()))
        conn.commit()
    except Exception as e:
        print(f"Error saving user: {e}")
    finally:
        conn.close()

def save_conversation(user_id, user_message, bot_response):
    """Log conversation to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO conversations
            (user_id, user_message, bot_response)
            VALUES (?, ?, ?)
        ''', (user_id, user_message, bot_response))
        conn.commit()
    except Exception as e:
        print(f"Error saving conversation: {e}")
    finally:
        conn.close()

def save_assessment(user_id, phq9_score, severity, answers):
    """Save assessment results"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO assessments
            (user_id, phq9_score, severity, answers)
            VALUES (?, ?, ?, ?)
        ''', (user_id, phq9_score, severity, str(answers)))
        conn.commit()
    except Exception as e:
        print(f"Error saving assessment: {e}")
    finally:
        conn.close()

def get_user_assessments(user_id):
    """Retrieve user's assessment history"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT phq9_score, severity, assessment_date 
            FROM assessments 
            WHERE user_id = ? 
            ORDER BY assessment_date DESC
        ''', (user_id,))
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error retrieving assessments: {e}")
        return []
    finally:
        conn.close()

if __name__ == "__main__":
    init_database()
