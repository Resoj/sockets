# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading

def handle_client(client_socket, client_id, addr):
    global gameData
    print(f"Accepted connection from {addr} with ID {client_id}")

    with lock:
        if client_id == 1:
            paddle = "left"
        elif client_id == 2:
            paddle = "right"
        init_data = f"{screenWidth},{screenHeight},{paddle}"
        client_socket.send(init_data.encode())
        gameData = client_socket.recv(1024).decode()

    while True:
        try:
            client_game_data = client_socket.recv(1024).decode()
            with lock:
                received_sync = int(client_game_data.split(',')[-1])

                if received_sync > int(gameData.split(',')[-1]):
                    gameData = client_game_data

                    for client in clients:
                        client.send(gameData.encode())

        except Exception as e:
            print(f"Error: {e}")
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "localhost"
port = 5050

screenWidth = 640
screenHeight = 480

server.bind((host, port))

server.listen(2)

print(f"Server is listening on {host}:{port}")

clients = []
client_id_counter = 0
lock = threading.Lock()

while True:
    client, addr = server.accept()
    client_id_counter += 1
    clients.append(client)
    client_thread = threading.Thread(target=handle_client, args=(client, client_id_counter, addr))
    client_thread.start()

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games