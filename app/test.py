from flask import Flask, request, jsonify
import sqlite3
import json
from datetime import datetime
import pandas as pd

DATABASE = 'sessions.db'
patient_id = '1234'
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()      
cursor.execute("SELECT start_time, end_time FROM sessions WHERE patient_id=?", (patient_id,))
rows = cursor.fetchall()
conn.close()

# if not rows:
    # return jsonify({'error': 'No sessions found for the patient'}), 404

# Debug print to inspect rows fetched from database
print(rows)

# Create a DataFrame from the rows
df = pd.DataFrame(rows, columns=['start_time', 'end_time'])

total_duration = 0
num_sessions = 0

for index, row in df.iterrows():
    # Convert the datetime strings to datetime objects and extract the time component
    start_time = datetime.fromisoformat(row['start_time'].replace('Z', '+00:00')).time()
    end_time = datetime.fromisoformat(row['end_time'].replace('Z', '+00:00')).time()
    
    # Calculate session duration in seconds
    start_datetime = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), end_time)
    
    # Ensure end time is always after start time
    if end_datetime < start_datetime:
        end_datetime += timedelta(days=1)
        
    session_duration = (end_datetime - start_datetime).total_seconds()
    
    total_duration += session_duration
    num_sessions += 1

average_duration = total_duration / num_sessions if num_sessions > 0 else 0
average_duration = average_duration /60


# return jsonify({'patient_id': patient_id, 'average_session_duration_seconds': average_duration}), 200