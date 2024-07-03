# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app /app

# Upgrade Werkzeug before installing other dependencies
# RUN pip install --upgrade Werkzeug

# Install Flask and other dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install --upgrade Flask Werkzeug
RUN pip install --upgrade numpy pandas
RUN pip cache purge


# Make port 5000 available to the world outside this container
EXPOSE 5000

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Use the entrypoint script to initialize the database and start the Flask app
ENTRYPOINT ["/entrypoint.sh"]
