import requests
import json

# URL of the Flask API
base_url = 'http://localhost:5001'

# Retrieve sessions for a patient
patient_id = "shawn"
response = requests.get(f'{base_url}/session_summary/{patient_id}')

# Check if the request was successful
if response.status_code == 200:
    # If the response status is OK, process the JSON data
    summary = response.json()
    print(json.dumps(summary, indent=2))
else:
    # If the response status is not OK, print the status code and response text
    print(f'Failed to retrieve session summary: {response.status_code}')
    print(response.text)
