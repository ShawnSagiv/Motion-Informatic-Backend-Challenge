#!/bin/bash

# docker run -p 5000:5000 -v /app:/app flask-app

docker run --platform linux/amd64 -p 5001:5000 -v /Users/shawnsagiv/Desktop/Challenge/app:/app flask-app