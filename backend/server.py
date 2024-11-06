import socket

# Server configuration
UDP_IP = "fly-global-services"      # This allows connections from any IP
UDP_PORT = 12345        # Use the port that Fly.io expects

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"UDP server is listening on {UDP_IP}:{UDP_PORT}")

while True:
    # Wait to receive a message from a client
    data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
    print(f"Received message: {data.decode()} from {addr}")
    
    # Send the message back to the client (echo)
    sock.sendto(data, addr)
    print(f"Echoed message back to {addr}")