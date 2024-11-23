import socket
import time
import random
import sqlite3
import sys

# Constants
UDP_IP = "0.0.0.0"
UDP_PORT = 12345
CLIENT_TIMEOUT = 5 * 60

# Database setup
DB_FILE = "performance.db"

def setup_db():
    """Create the database and tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            port INTEGER NOT NULL,
            rtt REAL,
            last_message_time REAL
        )
    ''')
    conn.commit()
    conn.close()

def reset_db():
    """Delete all records from the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM clients')
    conn.commit()
    conn.close()
    print("Database reset.")

def show_db():
    """Print all records from the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM clients')
    rows = c.fetchall()
    conn.close()
    print("Clients in database:")
    for row in rows:
        print(row)

# Check command-line arguments
if len(sys.argv) > 1:
    if sys.argv[1] == "reset":
        reset_db()
        sys.exit()
    elif sys.argv[1] == "show":
        show_db()
        sys.exit()

# Setup database and UDP server
setup_db()
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((UDP_IP, UDP_PORT))
udp.setblocking(False)

food = {}
clients = {}
print("Server started")

def generate_food():
    return {"x": random.randint(2, 47), "y": random.randint(2, 47)}

def update_client_in_db(ip, port, rtt):
    """Add or update a client in the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO clients (ip, port, rtt, last_message_time)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(ip, port) DO UPDATE SET
            rtt=excluded.rtt,
            last_message_time=excluded.last_message_time
    ''', (ip, port, rtt, time.time()))
    conn.commit()
    conn.close()

while True:
    try:
        data, addr = udp.recvfrom(1024)
        current_time = time.time()
        if data:
            message = data.decode('utf-8').strip()
            client_id = f"{addr[0]}:{addr[1]}"
            if client_id not in clients:
                clients[client_id] = {"ip": addr[0], "port": addr[1], "last_message_time": current_time}
            else:
                clients[client_id]["last_message_time"] = current_time

            if message.startswith("apple"):
                timestamp = int(message.split()[1])
                if food.get("timestamp") is None or food["timestamp"] < timestamp:
                    food = generate_food()
                    food["timestamp"] = timestamp
                    food_message = f"x={food['x']},y={food['y']},server_time={current_time}"
                    for client in clients.values():
                        udp.sendto(food_message.encode('utf-8'), (client["ip"], client["port"]))

            elif message == "Connect":
                if not food:
                    food = generate_food()
                food_message = f"x={food['x']},y={food['y']},server_time={current_time}"
                udp.sendto(food_message.encode('utf-8'), addr)

            elif message.startswith("RTT"):
                # Example RTT message: RTT 0.123
                try:
                    rtt = float(message.split()[1])
                    update_client_in_db(addr[0], addr[1], rtt)
                except ValueError:
                    print(f"Invalid RTT value from {client_id}")

    except BlockingIOError:
        pass

    # Remove inactive clients from memory
    current_time = time.time()
    for client_id in list(clients.keys()):
        if current_time - clients[client_id]["last_message_time"] > CLIENT_TIMEOUT:
            del clients[client_id]

    time.sleep(0.01)
