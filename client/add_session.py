import requests
import json
from datetime import datetime

# URL of the Flask API
base_url = 'http://localhost:5001'

def add_session():
    # Add a new session
    new_session = {
        "patient_id": "shawn",
        "session_id": "1",
        "start_time": "2023-07-01T12:00:00Z",
        "end_time": "2023-07-01T12:30:00Z",
        "movement_data": {
                            "movement_x": 9.6,
                            "movement_y": 9.2,
                            "movement_z": 30.1
                        } # Replace with the actual movement data
    }

    patient_id = new_session['patient_id']
    session_id = new_session['session_id']

   # Convert start and end times to datetime objects
    start_time = datetime.fromisoformat(new_session['start_time'].replace('Z', '+00:00'))
    end_time = datetime.fromisoformat(new_session['end_time'].replace('Z', '+00:00'))

    # Check if the start time is before the end time
    if start_time >= end_time:
        print("Error: The start time must be before the end time.")
        return
    
    # Check if the session ID already exists for the patient
    if session_is_exist(patient_id, session_id):
        print(f"Session ID {session_id} already exists for Patient ID {patient_id}. Cannot add session.")
        return


    response = requests.post(f'{base_url}/add_session', json=new_session)
    print(response.json())
    print("The session has been added successfully.")


def session_is_exist(patient_id, session_id):
    # Make a GET request to retrieve the session ID for the specified patient and session ID
    response = requests.get(f'{base_url}/check_session/{patient_id}/{session_id}')

    # Check if the request was successful
    if response.status_code == 200:
        try:
            data = response.json()
            # Check if the session ID exists in the response data
            if 'session_id' in data:
                return True
            else:
                return False
        except requests.exceptions.JSONDecodeError:
            print(f"Error: Non-JSON response received from {base_url}/get_session/{patient_id}/{session_id}")
            return False
    else:
        # print(f"Error: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    add_session()
    
