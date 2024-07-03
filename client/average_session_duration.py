import requests
import json

base_url = 'http://localhost:5001'
patient_id = "shawn"

response = requests.get(f'{base_url}/average_session_duration/{patient_id}')

# Check if the request was successful
if response.status_code == 200:
    # If the response status is OK, process the JSON data
    average_session_duration = response.json()
    print(average_session_duration)
else:
    # If the response status is not OK, print the status code and response text
    print(f'Failed to retrieve average session duration: {response.status_code}')
    print(response.text)
