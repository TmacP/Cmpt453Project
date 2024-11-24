import socket
import threading
import random
import time

TCP_HOST = '127.0.0.1'
TCP_PORT = 12345

# Global dictionary to store koi positions by ID
koi_positions = {}
lock = threading.Lock()

# Global list to track active client sockets
active_clients = []

# Fixed tick rate (e.g., 60 ticks per second)
TICK_RATE = 30 / 60.0  # 60 Hz (game tick every 1/60th of a second)

def handle_client(client_socket, address):
    global koi_positions
    global active_clients
    client_id = None

    try:
        print(f"New client connected from {address}")
        
        # Assign a new koi position for the client on connection
        client_id = str(address)  # Assign a unique client_id, can be address or custom ID
        
        # Randomize koi position for the client
        x = random.randint(0, 360)  # Random X position
        y = random.randint(0, 640)  # Random Y position
        koi_positions[client_id] = (x, y)
        print(f"Assigned koi position to {client_id}: {koi_positions[client_id]}")
        
        # Send the updated koi positions list to the client (excluding its own position)
        with lock:
            all_positions = "\n".join(
                f"{id}:{x},{y}" for id, (x, y) in koi_positions.items() if id != client_id
            )
            print(f"Sending all koi positions to {address}: {all_positions}")
        
        client_socket.sendall(all_positions.encode() + b"\n")
        
        # Add client socket to the active clients list
        with lock:
            active_clients.append(client_socket)
        
        while True:
            # Receive data from client (updates koi position)
            data = client_socket.recv(1024).decode()
            if not data:
                print(f"Client {address} disconnected (no data received).")
                break

            print(f"Received data from {address}: {data.strip()}")
            
            try:
                # Parse client ID and position from the received data
                client_id, pos = data.strip().split(":")
                x, y = map(float, pos.split(","))
                print(f"Client {client_id} sent position: ({x}, {y})")
                
                # Update koi position for the client
                with lock:
                    koi_positions[client_id] = (x, y)
                    print(f"Updated koi_positions with {client_id}: ({x}, {y})")
            
            except ValueError as e:
                print(f"Error parsing data from {address}: {e}")
                continue

            # Broadcast all koi positions to all clients except the sender
            with lock:
                all_positions = "\n".join(
                    f"{id}:{x},{y}" for id, (x, y) in koi_positions.items() if id != client_id
                )
                print(f"Sending all koi positions to {address}: {all_positions}")
            
            client_socket.sendall(all_positions.encode() + b"\n")

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
                print(f"Removed {client_id} from koi_positions")
        
        print(f"Client {address} disconnected")
        client_socket.close()


def game_tick():
    """Game tick function that updates koi positions and sends them to clients"""
    while True:
        time.sleep(TICK_RATE)
        
        with lock:
            # Example: Update each koi's position (you can adjust this logic as needed)
            for client_id, (x, y) in koi_positions.items():
                x += random.randint(-1, 1)  # Random horizontal movement
                y += random.randint(-1, 1)  # Random vertical movement
                koi_positions[client_id] = (x, y)
        
        with lock:
            all_positions = "\n".join(
                f"{id}:{x},{y}" for id, (x, y) in koi_positions.items()
            )
            print(f"Sending updated koi positions: {all_positions}")
        
        # Broadcast updated positions to all connected clients
        with lock:
            for client_socket in active_clients:
                try:
                    client_socket.sendall(all_positions.encode() + b"\n")
                except Exception as e:
                    print(f"Error sending to client: {e}")
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
            print(f"Connection established with {address}")
            threading.Thread(target=handle_client, args=(client_socket, address)).start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
