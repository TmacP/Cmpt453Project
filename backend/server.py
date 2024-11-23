import socket

TCP_HOST = '127.0.0.1'
TCP_PORT = 12345

def start_server():
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((TCP_HOST, TCP_PORT))
    server_socket.listen(1)

    print(f"Server started on {TCP_HOST}:{TCP_PORT}")

    while True:
        # Wait for a connection from a client
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        try:
            # Receive data sent by the client
            data = client_socket.recv(1024)
            if not data:
                print("No data received, closing connection.")
                break

            # Send the received data back to the client (echo)
            client_socket.sendall(data)
            print(f"Sent back: {data.decode()}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close the connection
            client_socket.close()

if __name__ == "__main__":
    start_server()
