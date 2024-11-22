import socket
import time
import random

UDP_IP = "0.0.0.0"
UDP_PORT = 12345
CLIENT_TIMEOUT = 5 * 60

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((UDP_IP, UDP_PORT))
udp.setblocking(False)

food = {}
clients = {}
print("Server started")

def generate_food():
    return {"x": random.randint(2, 47), "y": random.randint(2, 47)}

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

    except BlockingIOError:
        pass

    current_time = time.time()
    for client_id in list(clients.keys()):
        if current_time - clients[client_id]["last_message_time"] > CLIENT_TIMEOUT:
            del clients[client_id]

    time.sleep(0.01)
