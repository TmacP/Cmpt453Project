# Use the official Python 3 base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Python script to the container
COPY serverWS.py .

# Setup sqlite3 on a separate volume
RUN mkdir -p /data
VOLUME /data

# Copy the SQLite database to the container (initially, you could copy it, but once mounted, Fly.io will handle it)
COPY client_performance.db /data/client_performance.db

# Install the required Python dependencies
RUN pip install --no-cache-dir websockets





# Expose the port your application runs on
EXPOSE 12345

# Define the default command to run your application
CMD ["python3", "serverWS.py"]
