# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading

input_list = []

# Handles Sending Info to Clients
host ="localhost"
port = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

server.listen(2)

print(f"Server is listening on {host}:{port}")


# Handles Received Client
def handle_client(client_socket):

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        

        for client in input_list:
            if client != client_socket:
                client.send(data.encode())

        # Send message to every client
        print(data, end="\n")        
        response = "Server received: " + data
        client_socket.send(response.encode('utf-8'))
    client_socket.close()


while True:

    
    client, clientaddr = server.accept()

    print(f"Accepted connection from", clientaddr)

    input_list.append(client)

    client_handler = threading.Thread(target=handle_client, args=(client,))

    client_handler.start()






# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games