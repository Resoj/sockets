# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading
import time

sync_locks = threading.Lock()
input_locks = threading.Lock()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Handles Sending Info to Clients
host ="localhost"
port = 5050

inputList = []
DEBUGMODE = False
server.bind((host, port))

server.listen(3)
if DEBUGMODE:
    print(f"Server is listening on {host}:{port}")

syncs = [0,0]

# Handles Received Client
def handle_client(connection):
    if DEBUGMODE:
        print("sending to client at ", connection.getsockname(), "on port ", port)

    # INITIAL MESSAGE FOR CLIENT NUMBER
    
    while True:

        # Receive message from client
        if DEBUGMODE:
            print("Looking for message from client")
        fromClient = connection.recv(1024).decode('utf-8')
        # print(len(fromClient.split(",")))

        fromClient = fromClient.split("\n")[0]
        if DEBUGMODE:
            print("received from client: ", fromClient)

        if not fromClient:
            break
        
        else:
            parsedData = fromClient.split(",")
            # PaddlePosL, PaddlePosR, ballPos, score, sync

            # Conncection 1
            if connection == inputList[0][0]:
                with sync_locks:
                    syncs[0] = int(parsedData[-1])
            # Conncection 2
            if connection == inputList[1][0]:
                with sync_locks:
                    syncs[1] = int(parsedData[-1])
            
            if syncs[0] == 0 and syncs[1] == 0:
                with sync_locks:
                    if DEBUGMODE:
                        print("Both are zero")
                    continue

            elif syncs[0] > syncs[1]:
                # Update with data from connection 2
                if DEBUGMODE:
                    print("Client1 has a higher sync sending: ", fromClient, "to", inputList[1][0])

                fromClient = fromClient + "\n"
                inputList[1][0].send(fromClient.encode('utf-8'))
                                
        
            elif syncs[0] < syncs[1]:
                # Update with data from connection 1
                if DEBUGMODE:
                    print("Client 2 has a higher sync sending: ", fromClient, "to", inputList[0][0])
                fromClient = fromClient + "\n"
                inputList[0][0].send(fromClient.encode('utf-8'))

            else:
                fromClient = fromClient + "\n"
                inputList[0][0].send(fromClient.encode('utf-8'))
                inputList[1][0].send(fromClient.encode('utf-8'))


                
                
    connection.close()

ackCounter = 1
while True:

    client, clientaddr = server.accept()
    if DEBUGMODE:
        print(f"Accepted connection from", clientaddr)

    inputList.append([client,clientaddr, len(inputList)])
    if DEBUGMODE:
        print("Sending First ACK")

    client.send("ACK".encode('utf-8'))
    if DEBUGMODE:
        print("Waiting for HandShake")

    acknowledgment = client.recv(1024).decode('utf-8')

    if acknowledgment == "ACK":
        if DEBUGMODE:
            print("Received ACK", ackCounter)

        if ackCounter < 3:

            ackCounter += 1
    if DEBUGMODE:
        print("Sending client number: ", str(len(inputList)))
    toClient = client.send(str(len(inputList)).encode('utf-8'))
    


    with input_locks:
        if len(inputList) == 1:
            if DEBUGMODE:
                print("Starting First Thread")

            client_handler1 = threading.Thread(target=handle_client, args=(client,)) 

        if len(inputList) == 2:
            
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start()
            client_handler1.start()







# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games