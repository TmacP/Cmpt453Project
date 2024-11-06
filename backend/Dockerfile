# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the server script into the container
COPY server.py .

# Expose the UDP port the server will use
EXPOSE 12345/tcp

# Run the server script
CMD ["python", "server.py"]
