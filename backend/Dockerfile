# Use an official Alpine image as a base, as it’s lightweight and easy to install Lua on
FROM python3

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Lua server script into the container
COPY server.py .

# Expose the UDP port the server will use
EXPOSE 12345/udp

# Run the server script
CMD ["python3", "server.py"]
