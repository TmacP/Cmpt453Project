import socket
import random

# Server configuration
UDP_IP = "fly-global-services"  # This allows connections from any IP
UDP_PORT = 12345  # Use the port that Fly.io expects

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Function to generate random food position
def generate_food():
    return {"x": random.randint(2, 47), "y": random.randint(2, 47)}

# Track the food position
# Initialize food as an empty dictionary
food = {}
clients = set()


while True:
    # Wait to receive a message from a client
    data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
    message = data.decode()  # Decode the message

    # Keep track of clients that have connected
    clients.add(addr)

    if message == "debug":
        food_message = f"x={food['x']},y={food['y']}"
        client_list = ", ".join([f"{client[0]}:{client[1]}" for client in clients])  # Format clients as IP:Port
        response_message = f"Food Position: {food_message}\nConnected Clients: {client_list}"
        
        sock.sendto(response_message.encode(), addr)


    elif message == "apple":
        # Generate new food position and send it to all clients
        food = generate_food()  # Update the food position
        food_message = f"x={food['x']},y={food['y']}"
        for client in clients:
            sock.sendto(food_message.encode(), client)

    elif message in ["up", "down", "left", "right"]:
        # Optionally, echo the received message back to the client
        sock.sendto(data, addr)

    elif message == "Connect":
        # If there is no apple, create the first one
        if not food:
            food = generate_food()
        
        food_message = f"x={food['x']},y={food['y']}"
        # Send the food position to the connecting client (addr)
        sock.sendto(food_message.encode(), addr)