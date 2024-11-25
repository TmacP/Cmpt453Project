import asyncio
import websockets

# This is a basic handler that accepts a connection and sends a message
async def handler(websocket, path):
    print(f"New connection from {websocket.remote_address}")
    
    # Receive messages from the client
    async for message in websocket:
        print(f"Received: {message}")  # Log the received message (timestamp)
        
        # Send back the same message (timestamp) to the client
        await websocket.send(message)
        print(f"Sent: {message}")  # Log the sent message (timestamp)
    
    # Keep the connection open (wait for the client to close it)
    await websocket.wait_closed()

# Start the WebSocket server
async def start_server():
    server = await websockets.serve(handler, "localhost", 8765)
    print("WebSocket server started at ws://localhost:8765")
    await server.wait_closed()

# Run the server
asyncio.run(start_server())
