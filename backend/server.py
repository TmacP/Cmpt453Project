import socket
import time
import random

# Server configuration
UDP_IP = "0.0.0.0"  # Listening on all IP addresses
UDP_PORT = 12345

# Timeout configuration (5 minutes)
CLIENT_TIMEOUT = 5 * 60  # 5 minutes in seconds

# Create a UDP socket and bind it to the server address
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((UDP_IP, UDP_PORT))
udp.setblocking(False)  # Non-blocking mode

# Function to generate random food position
def generate_food():
    return {"x": random.randint(2, 47), "y": random.randint(2, 47)}

# Initialize food and client tracking
food = {}
clients = {}

print("Begin server")

while True:
    try:
        # Wait to receive a message from a client
        data, addr = udp.recvfrom(1024)  # Buffer size of 1024 bytes
        current_time = time.time()

        if data:
            message = data.decode('utf-8').strip()  # Decode and strip whitespace
            print(f"Received message: {message} from {addr}")

            # Keep track of clients that have connected
            client_id = f"{addr[0]}:{addr[1]}"
            if client_id not in clients:
                print(f"New client connected: {client_id}")
                clients[client_id] = {"ip": addr[0], "port": addr[1], "last_message_time": current_time}
            else:
                # Update the last message time for the existing client
                clients[client_id]["last_message_time"] = current_time

            if message == "apple":
                # Generate new food position and send it to all clients
                food = generate_food()
                food_message = f"x={food['x']},y={food['y']}"
                print(f"Generated new food position: {food_message}")
                for client in clients.values():
                    print(f"Sending food position to client: {client['ip']}:{client['port']}")
                    udp.sendto(food_message.encode('utf-8'), (client["ip"], client["port"]))

            elif message in ["up", "down", "left", "right"]:
                # Echo the received message back to the client
                print(f"Echoing move command: {message}")
                udp.sendto(data, addr)

            elif message == "Connect":
                # If there is no apple, create the first one
                if not food:
                    food = generate_food()
                    print(f"First apple created: x={food['x']}, y={food['y']}")
                food_message = f"x={food['x']},y={food['y']}"
                print(f"Sending food position to new client: {food_message}")
                udp.sendto(food_message.encode('utf-8'), addr)

    except BlockingIOError:
        # No data available; continue the loop
        pass

    # Remove clients who haven't sent a message in the last 5 minutes
    current_time = time.time()
    for client_id in list(clients.keys()):  # Use list to avoid runtime error while modifying dictionary
        if current_time - clients[client_id]["last_message_time"] > CLIENT_TIMEOUT:
            print(f"Client {client_id} has been inactive for 5 minutes. Removing.")
            del clients[client_id]

    time.sleep(0.01)  # Small delay to reduce CPU usage
