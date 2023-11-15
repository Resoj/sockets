# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Handles Sending Info to Clients
host ="localhost"
port = 5050

inputList = []

server.bind((host, port))

server.listen(3)

print(f"Server is listening on {host}:{port}")
syncs = [0,0]
# Handles Received Client
def handle_client(connection):

    print("sending to client at ", connection.getsockname(), "on port ", port,)

    while True:
 
        # Send message to client
        

        toClient = connection.send("Welcome to the server".encode())

        # Receive message from client
        fromClient = connection.recv(1024).decode()
        if not fromClient:
            break
        else:
            
            parsedData = fromClient.split(',')
            # PaddlePosL, PaddlePosR, ballPos, score, sync

            if connection == inputList[0]:
                print("\nfrom Connection 1")
                print(parsedData[-1])
                syncs[0] = int(parsedData[-1])
            if connection == inputList[1]:
                print("\nfrom Connection 2")
                print(parsedData[-1])
                syncs[1] = int(parsedData[-1])
            
            if syncs[0] == 0 and syncs[1] == 0:
                continue
            if syncs[0] > syncs[1]:
                # Update with data from connection 1
                inputList[0].send(fromClient.encode('utf-8'))




        
        # Send message to every client
        # response = "Server received: " + fromClient
        connection.send(fromClient.encode('utf-8'))
    connection.close()


while True:

    
    client, clientaddr = server.accept()

    print(f"Accepted connection from", clientaddr)

    inputList.append(client)

    client_handler = threading.Thread(target=handle_client, args=(client,))

    client_handler.start()

    print("\n", client, " is threading")






# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games