import socket
import threading
import time

TCP_HOST = '127.0.0.1'
TCP_PORT = 12345

# Global dictionary to store koi positions by ID
koi_positions = {}
lock = threading.Lock()

def handle_client(client_socket, address):
    global koi_positions
    client_id = None

    try:
        print(f"New client connected from {address}")
        
        # Assign a new koi position for the client on connection
        client_id = str(address)  # Assign a unique client_id, can be address or custom ID
        
        # Default koi position, could be randomized or predefined
        koi_positions[client_id] = (100, 200)  # Assign a default starting position
        print(f"Assigned koi position to {client_id}: {koi_positions[client_id]}")
        
        # Send the updated koi positions list to the client
        with lock:
            all_positions = "\n".join(
                f"{id}:{x},{y}" for id, (x, y) in koi_positions.items()
            )
            print(f"Sending all koi positions to {address}: {all_positions}")
        
        client_socket.sendall(all_positions.encode() + b"\n")
        
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

            # Broadcast all koi positions to the client
            with lock:
                all_positions = "\n".join(
                    f"{id}:{x},{y}" for id, (x, y) in koi_positions.items()
                )
                print(f"Sending all koi positions to {address}: {all_positions}")
            
            client_socket.sendall(all_positions.encode() + b"\n")

    except Exception as e:
        print(f"Error with client {address}: {e}")
    finally:
        # Remove koi when client disconnects
        with lock:
            if client_id in koi_positions:
                del koi_positions[client_id]
                print(f"Removed {client_id} from koi_positions")
        print(f"Client {address} disconnected")
        client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((TCP_HOST, TCP_PORT))
    server_socket.listen(5)

    print(f"Server started on {TCP_HOST}:{TCP_PORT}")
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
