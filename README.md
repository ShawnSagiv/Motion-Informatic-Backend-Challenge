# Motion Informatics Backend Challenge

## Background

We are working on a cutting-edge project aimed at rehabilitating disordered hand movements in patients using advanced technology. Our system involves the STIMEL-03, a stimulation unit that interacts with the hand muscles using electrodes to read and stimulate the patient's brain neuron activity, an AR headset to present content to the patient to encourage hand movement, and data from the AR headset sensors to monitor actual hand movement.

## Installation

1. build the docker-image using build.sh script or pull it from artifactory (if we have we can push it)
NOTE!: the build script is to build it locally on macOS machine. for other OS need adjustment according. 
2. deploy the system using deploy.sh script. 
NOTE!: you need port 5001 will be available on the hosted machine. 
3. entrypoint.sh is the deploy entrypoint, which upload the DB and the flask server. 

## Clone the repository.

# API Endpoints
## The project includes the following API endpoints:
## you can use the scripts in the client folder for easy start. 

EXAMPLE: path/to/installed/python client/add_session.py

1. /add_session: Adds a new session to the database.
Example request: {
        "patient_id": "shawn", 
        "session_id": "1",
        "start_time": "2023-07-01T12:00:00Z",
        "end_time": "2023-07-01T12:30:00Z",
        "movement_data": {
                        "movement_x": 9.6,
                        "movement_y": 9.2,
                        "movement_z": 30.1
                        } # Replace with the actual movement data

2. /get_sessions: Get all sessions for a specific patient
3. /average_session_duration: Get average session duration
4. /session_summary: Generate a summary report for a given patient

NOTE!: in all the other 3 request need to add 'patient_id'. 

# validation rules
1. "patient_id" is uniqe to each patient - can't be 2 patient with the same "patient_id".
2. "session_id" is uniqe per patient - can't be 2 "session_id" with the same seriel number.
3. "start_time" & "end_time" must be syncronized. 
4. "movement_data" is in JSON format as presented above. 
