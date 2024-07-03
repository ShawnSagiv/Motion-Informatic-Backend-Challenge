import requests
import json

# URL of the Flask API
base_url = 'http://localhost:5001'


# Add a new session
new_session = {
    "patient_id": "1234",
    "session_id": "3",
    "start_time": "2023-07-01T12:00:00Z",
    "end_time": "2023-07-01T12:30:00Z",
    # "movement_data": {"movement": "example"}
    # "movement_data": json.dumps({"movement": "example"})
    "movement_data": {"movement": "example"}
}

# response = requests.get(f'{base_url}/check_session/{new_session["session_id"]}')

response = requests.get(f'{base_url}/get_sessions/{new_session["session_id"]}')
print (response.json())



# if response.status_code == 200:
#     print("Session ID already exists. Cannot proceed with the POST request.")
# else:
#     # Proceed with the POST request
#     response = requests.post(f'{base_url}/add_session', json=new_session)
#     print(response.json())

# Retrieve sessions for a patient
# patient_id = "1234"
# response = requests.get(f'{base_url}/get_sessions/{patient_id}')
# print(response.json())
