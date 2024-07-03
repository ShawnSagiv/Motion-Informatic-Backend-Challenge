from flask import Flask, request, jsonify
import sqlite3
import json
from datetime import datetime
import pandas as pd

app = Flask(__name__)
DATABASE = 'sessions.db'

# connect to the database helper
def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

# add a new session
@app.route('/add_session', methods=['POST'])
def add_session():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (patient_id, session_id, start_time, end_time, movement_data) VALUES (?, ?, ?, ?, ?)",
                   (data['patient_id'], data['session_id'], data['start_time'], data['end_time'], json.dumps(data['movement_data'])))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'}), 201

# get all sessions for specific patient
@app.route('/get_sessions/<patient_id>', methods=['GET'])
def get_sessions(patient_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions WHERE patient_id=?", (patient_id,))
    rows = cursor.fetchall()
    conn.close()
    sessions = [{'patient_id': row[0], 'session_id': row[1], 'start_time': row[2], 'end_time': row[3], 'movement_data': json.loads(row[4])} for row in rows]
    return jsonify(sessions), 200


# check if session exists (helper function)
@app.route('/check_session/<patient_id>/<session_id>', methods=['GET'])
def check_session(patient_id, session_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT session_id FROM sessions WHERE patient_id=? AND session_id=?", (patient_id, session_id))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        session_id_found = result[0]
        return jsonify({'session_id': session_id_found}), 200
    else:
        return jsonify({'error': 'Session not found'}), 404

# get average session duration
@app.route('/average_session_duration/<patient_id>', methods=['GET'])
def average_session_duration(patient_id):
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT start_time, end_time FROM sessions WHERE patient_id=?", (patient_id,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return jsonify({'error': 'No sessions found for the patient'}), 404

    # Create a DataFrame from the rows - for comfortable use
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
        
        # Calculate session duration in seconds
        session_duration = (end_datetime - start_datetime).total_seconds()
        
        total_duration += session_duration
        num_sessions += 1
    # calculate average session duration in minutes
    average_duration = total_duration / num_sessions if num_sessions > 0 else 0
    average_duration = average_duration/60 

    return jsonify({'patient_id': patient_id, 'average_session_duration_seconds': average_duration}), 200

# Generate a summary report for a given patient
@app.route('/session_summary/<patient_id>', methods=['GET'])
def session_summary(patient_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT start_time, end_time, movement_data FROM sessions WHERE patient_id=?", (patient_id,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return jsonify({'error': 'No sessions found for the patient'}), 404

    # Create a DataFrame from the rows
    df = pd.DataFrame(rows, columns=['start_time', 'end_time', 'movement_data'])

    # Calculate the total number of sessions
    total_sessions = len(df)

    # Calculate the average movement data
    # Assuming movement_data is a dictionary with numeric values (presents in the add_session function)
    movement_data_list = [json.loads(md) for md in df['movement_data']]
    avg_movement_data = pd.DataFrame(movement_data_list).mean().to_dict()

    # Find the date of the first and last session
    first_session_date = min(df['start_time'])
    last_session_date = max(df['end_time'])

    summary = {
        'patient_id': patient_id,
        'total_sessions': total_sessions,
        'average_movement_data': avg_movement_data,
        'first_session_date': first_session_date,
        'last_session_date': last_session_date
    }

    return jsonify(summary), 200




if __name__ == '__main__':
    app.run(debug=True)
