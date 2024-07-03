import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('sessions.db')
cursor = conn.cursor()

# Check if 'sessions' table already exists
cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='sessions' ''')
if cursor.fetchone()[0] == 1:
    print('Table sessions already exists.')
else:
    # Create 'sessions' table if it does not exist
    cursor.execute('''
        CREATE TABLE sessions (
            patient_id TEXT,
            session_id INTEGER,
            start_time TEXT,
            end_time TEXT,
            movement_data JSON,
            PRIMARY KEY (patient_id, session_id)
        )
    ''')
    print('Table sessions created.')

# Commit changes and close connection
conn.commit()
conn.close()
