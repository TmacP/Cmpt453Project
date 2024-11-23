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
        while True:
            # Receive data from client
            data = client_socket.recv(1024).decode()
            if not data:
                break

            print(f"Received: {data.strip()} from {address}")
            # Parse koi data
            client_id, pos = data.strip().split(":")
            x, y = map(float, pos.split(","))

            # Update koi positions in thread-safe way
            with lock:
                koi_positions[client_id] = (x, y)

            # Broadcast all koi positions to the client
            with lock:
                all_positions = "\n".join(
                    f"{id}:{x},{y}" for id, (x, y) in koi_positions.items()
                )
            client_socket.sendall(all_positions.encode() + b"\n")

    except Exception as e:
        print(f"Error with client {address}: {e}")
    finally:
        # Remove koi on disconnect
        with lock:
            if client_id in koi_positions:
                del koi_positions[client_id]
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
            print(f"Connection from {address}")
            threading.Thread(target=handle_client, args=(client_socket, address)).start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
