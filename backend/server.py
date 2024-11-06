import socket
import random

# Server configuration
UDP_IP = "fly-global-services"      # This allows connections from any IP
UDP_PORT = 12345        # Use the port that Fly.io expects

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Function to generate random food position
def generate_food():
    return {"x": random.randint(2, 47), "y": random.randint(2, 47)}

# Track the food position
food = generate_food()

while True:
    # Wait to receive a message from a client
    data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
    message = data.decode()  # Decode the message

    if message == "debug":
        # Send the food position to the client as a string (e.g., "x=5,y=10")
        food_message = f"x={food['x']},y={food['y']}"
        sock.sendto(food_message.encode(), addr)


    elif message in ["up", "down", "left", "right", "Connect"]:
        # Optionally, echo the received message back to the client
        sock.sendto(data, addr)
