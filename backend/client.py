import socket

# Server details
TCP_HOST = '127.0.0.1'
TCP_PORT = 12345

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((TCP_HOST, TCP_PORT))
    print("Connected to server")

    # Send the message
    message = "foobar"
    client_socket.send(message.encode())
    print(f"Sent: {message}")

    # Receive the response
    response = client_socket.recv(1024).decode()
    print(f"Received: {response}")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the socket
    client_socket.close()


