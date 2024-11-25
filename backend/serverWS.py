#!/usr/bin/env python

"""Echo server with client tracking using the asyncio API."""

import asyncio
from websockets.asyncio.server import serve

# A set to keep track of connected clients
connected_clients = {}

async def echo(websocket):
    # Register the new client
    if websocket not in connected_clients:
        connected_clients[websocket] = (0, 0)  # Initial position
        print(f"New client connected. Total clients: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            # Log the received message
            #print(f"Received from client: {message}")
            
            # Prepare the response: append all client coordinates to the echoed message
            client_positions = [
                {"id": id(client), "coords": coords}
                for client, coords in connected_clients.items()
            ]
            
            # The response includes the original message and the client positions
            response = {
                "message": message,
                "clients": client_positions
            }
            
            # Send the response back to the client
            await websocket.send(str(response))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Unregister the client when disconnected
        # Remove the client on disconnect
        connected_clients.pop(websocket, None)
        print(f"Client disconnected. Total clients: {len(connected_clients)}")

async def main():
    async with serve(echo, "0.0.0.0", 12345) as server:
        print("Server started, listening on ws://0.0.0.0:12345")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
