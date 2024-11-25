# Use the official Python 3 base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Python script to the container
COPY serverWS.py .

# Install the required Python dependencies
RUN pip install --no-cache-dir websockets

# Expose the port your application runs on
EXPOSE 8765

# Define the default command to run your application
CMD ["python3", "serverWS.py"]
