import socket
import threading
import random
import time
import math

UDP_HOST = '0.0.0.0'
UDP_PORT = 12345

# Global dictionary to store koi positions by ID
koi_positions = {}
# Global dictionary to store koi current targets
koi_targets = {}
lock = threading.Lock()

# Global list to track active client addresses
active_clients = []

# Fixed tick rate (e.g., 60 ticks per second)
TICK_RATE = 1 / 60.0  # 60 Hz (game tick every 1/60th of a second)

# Fish movement settings
MOVE_SPEED = 1  # How fast the fish moves towards the target

def get_random_target():
    """Return a random position within the screen boundaries"""
    return random.randint(0, 360), random.randint(0, 640)

def move_towards_target(current_x, current_y, target_x, target_y):
    """Move the fish towards the target position."""
    # Calculate the distance between the current position and the target position
    dx = target_x - current_x
    dy = target_y - current_y
    distance = math.sqrt(dx**2 + dy**2)

    if distance == 0:
        return current_x, current_y

    # Calculate the movement step
    move_step_x = (dx / distance) * MOVE_SPEED
    move_step_y = (dy / distance) * MOVE_SPEED

    # Update the position towards the target
    new_x = current_x + move_step_x
    new_y = current_y + move_step_y

    # If we're very close to the target, snap the fish to the target
    if distance < MOVE_SPEED:
        new_x, new_y = target_x, target_y

    return new_x, new_y

def handle_client(client_address):
    global koi_positions
    global koi_targets
    client_id = None

    try:
        # Assign a new koi position for the client on connection
        client_id = str(client_address)  # Assign a unique client_id, can be address or custom ID
        
        # Randomize koi position for the client
        x, y = get_random_target()
        koi_positions[client_id] = (x, y)
        # Assign a random target as well
        target_x, target_y = get_random_target()
        koi_targets[client_id] = (target_x, target_y)

        # Add client address to the active clients list
        with lock:
            active_clients.append(client_address)

        while True:
            # Simulate receiving data from client (could be timestamp or other updates)
            time.sleep(TICK_RATE)

            with lock:
                # Broadcast updated positions to all connected clients
                all_positions = "\n".join(
                    f"{id}:{x},{y}" for id, (x, y) in koi_positions.items() if id != client_id
                )

            # Send all koi positions to the client
            # Broadcast to all active clients
            with lock:
                for client in active_clients:
                    try:
                        # Send data via UDP (client_address is used for sending to specific clients)
                        server_socket.sendto(all_positions.encode(), client)
                    except Exception as e:
                        active_clients.remove(client)

    except Exception as e:
        print(f"Error with client {client_address}: {e}")
    finally:
        # Remove koi position when client disconnects
        with lock:
            if client_id in koi_positions:
                del koi_positions[client_id]
                del koi_targets[client_id]
        
        print(f"Client {client_address} disconnected")

def game_tick():
    """Game tick function that updates koi positions and sends them to clients"""
    while True:
        time.sleep(TICK_RATE)
        
        with lock:
            # Example: Update each koi's position (move towards random targets)
            for client_id, (x, y) in koi_positions.items():
                target_x, target_y = koi_targets[client_id]
                
                # Move the fish towards its target
                new_x, new_y = move_towards_target(x, y, target_x, target_y)
                koi_positions[client_id] = (new_x, new_y)

                # If fish is near the target, pick a new random target
                if math.sqrt((new_x - target_x) ** 2 + (new_y - target_y) ** 2) < MOVE_SPEED:
                    koi_targets[client_id] = get_random_target()

def start_server():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((UDP_HOST, UDP_PORT))

    print(f"Server started on {UDP_HOST}:{UDP_PORT}")
    
    # Start the game tick thread
    threading.Thread(target=game_tick, daemon=True).start()
    
    try:
        while True:
            data, client_address = server_socket.recvfrom(1024)
            print(f"Received data from {client_address}: {data.decode()}")
            threading.Thread(target=handle_client, args=(client_address,)).start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
