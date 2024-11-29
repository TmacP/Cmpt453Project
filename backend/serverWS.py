#!/usr/bin/env python

"""Echo server with client tracking using the asyncio API."""

import asyncio
from websockets.server import serve

import ssl
import sqlite3
import re
import time

# A set to keep track of connected clients
connected_clients = {}

# Regular expressions for matching different message formats
TIME_PATTERN = r"Timestamp: ([\d.]+)"
ID_PATTERN = r"Client ID: (\d+)"
POS_PATTERN = r"Koi Position: \(([\d.]+), ([\d.]+)\)"
ANGLE_PATTERN = r"Koi Angle: (-?\d+(\.\d*)?)"
ROUND_TRIP_TIME = r"RTT: ([\d.]+)"

# Store performance data for periodic write to DB
performance_data_to_write = []

# Function to initialize SQLite database
def init_db():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('client_performance.db')
    cursor = conn.cursor()

    # Create a table to store client performance data if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS performance_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_id TEXT,
                        rtt REAL,
                        num_clients INTEGER,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')
    conn.commit()
    conn.close()

# Function to insert client performance data into the database
def insert_performance_data(client_id, rtt, num_clients):
    conn = sqlite3.connect('client_performance.db')
    cursor = conn.cursor()

    # Insert the data into the performance_data table
    cursor.execute('''INSERT INTO performance_data (client_id, rtt, num_clients)
                      VALUES (?, ?, ?)''', (client_id, rtt, num_clients))

    conn.commit()
    conn.close()

# Function to periodically write the performance data to DB
async def write_performance_data():
    global performance_data_to_write
    while True:
        # Wait for 1 second to accumulate data
        await asyncio.sleep(1)

        # Write collected data to the DB
        for data in performance_data_to_write:
            client_id, rtt, num_clients = data
            insert_performance_data(client_id, rtt, num_clients)
            print(f"Inserted data into DB: Client ID = {client_id}, RTT = {rtt}, Number of Clients = {num_clients}")

        # Clear the list after writing to DB
        performance_data_to_write.clear()

async def echo(websocket):
    # Register the new client
    if websocket not in connected_clients:
        connected_clients[websocket] = {'pos': (0, 0), 'angle': 0}  # Initial position and angle
        print(f"New client connected. Total clients: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            # Log the received message
            message = message.decode("utf-8")
            
            # Initialize matches as None
            time_match = None
            id_match = None
            pos_match = None
            angle_match = None
            rtt_match = None

            # Check for the different message patterns
            time_match = re.search(TIME_PATTERN, message)
            id_match = re.search(ID_PATTERN, message)
            pos_match = re.search(POS_PATTERN, message)
            angle_match = re.search(ANGLE_PATTERN, message)
            rtt_match = re.search(ROUND_TRIP_TIME, message)

            # If RTT and Client ID are found, we process them
            if rtt_match and id_match:
                client_id = id_match.group(1)  # Extract Client ID
                rtt_value = float(rtt_match.group(1))  # Extract RTT

                # Get the number of connected clients
                num_clients = len(connected_clients)

                # Store the performance data for periodic DB writes
                #performance_data_to_write.append((client_id, rtt_value, num_clients))

            # Update position if both ID and Position are found in the message
            if id_match and pos_match and angle_match:
                client_id = id_match.group(1)  # Extract Client ID
                koi_pos_x = float(pos_match.group(1))  # Extract Koi Position X
                koi_pos_y = float(pos_match.group(2))  # Extract Koi Position Y
                koi_angle = float(angle_match.group(1))

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
                "message": message,  # the echoed timestamp to calculate rtt
                "your_id": id(websocket),  # Include the client's ID
                "clients": client_positions  # the list of the clients, and their positions
            }
            
            # Send the response back to the client
            await websocket.send(str(response))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Unregister the client when disconnected
        connected_clients.pop(websocket, None)
        print(f"Client disconnected. Total clients: {len(connected_clients)}")

async def main():
    # Initialize the database
    init_db()

    # Start the periodic write task
    asyncio.create_task(write_performance_data())

    # Create SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")  # Use your certificate and key files

    # Start the server with SSL
    async with serve(echo, "0.0.0.0", 12345, ssl=ssl_context) as server:
        print("Server started")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
