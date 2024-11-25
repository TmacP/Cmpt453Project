import socket
import threading
import random
import time
import math

TCP_HOST = '0.0.0.0'
TCP_PORT = 12345

# Global dictionary to store koi positions by ID
koi_positions = {}
# Global dictionary to store koi current targets
koi_targets = {}
lock = threading.Lock()

# Global list to track active client sockets
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

def handle_client(client_socket, address):
    global koi_positions
    global koi_targets
    global active_clients
    client_id = None

    try:
        # Assign a new koi position for the client on connection
        client_id = str(address)  # Assign a unique client_id, can be address or custom ID
        
        # Randomize koi position for the client
        x, y = get_random_target()
        koi_positions[client_id] = (x, y)
        # Assign a random target as well
        target_x, target_y = get_random_target()
        koi_targets[client_id] = (target_x, target_y)

        # Send the updated koi positions list to the client (excluding its own position)
        with lock:
            all_positions = "\n".join(
                f"{id}:{x},{y}" for id, (x, y) in koi_positions.items() if id != client_id
            )
        
        client_socket.sendall(all_positions.encode() + b"\n")
        
        # Add client socket to the active clients list
        with lock:
            active_clients.append(client_socket)
        
        while True:
            # Receive data from client (updates koi position)
            data = client_socket.recv(1024).decode()

            print(f"Received data from {address}: {data}")
            
            try:
                # Check if the data has both a client_id and timestamp (split by ":")
                print(data)

                timestamp = data.strip()
                print(f"Client {client_id} sent timestamp: ({timestamp})")  
                

                # Send the timestamp back to the client
                client_socket.sendall(f"Received your timestamp: {timestamp}\n".encode())
                

                # Broadcast all koi positions to all clients
                client_socket.sendall(all_positions.encode() + b"\n")
     
            except ValueError as e:
                print(f"Error parsing data from {address}: {e}")
                continue  # Skip to the next iteration if data format is incorrect

    except Exception as e:
        print(f"Error with client {address}: {e}")
    finally:
        # Remove client socket from active clients list
        with lock:
            if client_socket in active_clients:
                active_clients.remove(client_socket)
        
        # Remove koi position when client disconnects
        with lock:
            if client_id in koi_positions:
                del koi_positions[client_id]
                del koi_targets[client_id]
        
        print(f"Client {address} disconnected")
        client_socket.close()



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
        
        with lock:
            all_positions = "\n".join(
                f"{id}:{x},{y}" for id, (x, y) in koi_positions.items()
            )
        
        # Broadcast updated positions to all connected clients
        with lock:
            for client_socket in active_clients:
                try:
                    client_socket.sendall(all_positions.encode() + b"\n")
                except Exception as e:
                    active_clients.remove(client_socket)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((TCP_HOST, TCP_PORT))
    server_socket.listen(5)

    print(f"Server started on {TCP_HOST}:{TCP_PORT}")
    
    # Start the game tick thread
    threading.Thread(target=game_tick, daemon=True).start()
    
    try:
        while True:
            client_socket, address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, address)).start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
