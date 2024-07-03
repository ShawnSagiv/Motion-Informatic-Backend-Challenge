import requests
import json

# URL of the Flask API
base_url = 'http://localhost:5001'

# Retrieve sessions for a patient
patient_id = "shawn"
response = requests.get(f'{base_url}/get_sessions/{patient_id}')

# Check if the request was successful
if response.status_code == 200:
    # If the response status is OK, process the JSON data
    sessions = response.json()
    print(sessions)
else:
    # If the response status is not OK, print the status code and response text
    print(f'Failed to retrieve sessions: {response.status_code}')
    print(response.text)
