#!/usr/bin/env python

import asyncio
import re
import http
import signal
from websockets.asyncio.server import serve

# A dictionary to keep track of connected clients
connected_clients = {}

# Regular expressions for matching different message formats
TIME_PATTERN = r"Timestamp: ([\d.]+)"
ID_PATTERN = r"Client ID: (\d+)"
POS_PATTERN = r"Koi Position: \(([\d.]+), ([\d.]+)\)"
ANGLE_PATTERN = r"Koi Angle: (-?\d+(\.\d*)?)"

async def echo(websocket):
    # Register the new client
    if websocket not in connected_clients:
        connected_clients[websocket] = {'pos': (0, 0), 'angle': 0}  # Initial position and angle
        print(f"New client connected. Total clients: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            # Decode the received message
            message = message.decode("utf-8")
            
            # Initialize matches as None
            time_match = None
            id_match = None
            pos_match = None
            angle_match = None

            # Check for the different message patterns
            time_match = re.search(TIME_PATTERN, message)
            id_match = re.search(ID_PATTERN, message)
            pos_match = re.search(POS_PATTERN, message)
            angle_match = re.search(ANGLE_PATTERN, message)
            
            # Update position if both ID and Position are found in the message
            if id_match and pos_match and angle_match:
                client_id = id_match.group(1)  # Extract Client ID
                koi_pos_x = float(pos_match.group(1))  # Extract Koi Position X
                koi_pos_y = float(pos_match.group(2))  # Extract Koi Position Y
                koi_angle = float(angle_match.group(1))  # Extract Angle

                print(f"Updating Client ID: {client_id}, Koi Position: ({koi_pos_x}, {koi_pos_y}), Angle: {koi_angle}")
                
                # Update the connected client's position and angle
                connected_clients[websocket] = {'pos': (koi_pos_x, koi_pos_y), 'angle': koi_angle}

            # Prepare the response: append all client coordinates and angles to the echoed message
            client_positions = [
                {"id": id(client), "coords": coords['pos'], "angle": coords['angle']}
                for client, coords in connected_clients.items()
            ]
            
            # The response includes the original message and the client positions
            response = {
                "your_id": id(websocket),  # Include the client's ID
                "clients": client_positions  # The list of the clients, and their positions
            }
            print(f"Response: {response}")
            # Send the response back to the client
            await websocket.send(str(response))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Unregister the client when disconnected
        connected_clients.pop(websocket, None)
        print(f"Client disconnected. Total clients: {len(connected_clients)}")

async def health_check(connection, request):
    if request.path == "/healthz":
        return connection.respond(http.HTTPStatus.OK, "OK\n")

async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    # Start the server
    async with serve(
        echo,
        host="0.0.0.0",
        port=12345,
        process_request=health_check,
    ):
        print("Server started")
        await stop

if __name__ == "__main__":
    asyncio.run(main())
