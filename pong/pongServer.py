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

# Lock Setup
input_locks = [threading.Lock(), threading.Lock()]
sync_locks = [threading.Lock(), threading.Lock()]
syncs = [0,0]

# Initial Socket Setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Hosts and Ports
# host ="10.113.32.29"
host = "localhost"
port = 5050

# client and client address storage
inputList = []

# Mode for Debugging ( lessens printing in console)
DEBUGMODE = True

server.bind((host, port))
server.listen(3)

if DEBUGMODE:
    print(f"Server is listening on {host}:{port}")

def handle_client(connection):
    # Purpose : to handle client threads

    if DEBUGMODE:
        print("sending to client at ", connection.getsockname(), "on port ", port)

    # Main Client loop
    while True:

        if DEBUGMODE:
            print("Looking for message from client")

        # Parsing operations
        with input_locks[0]:
            
            fromClient1 = connection.recv(1024).decode('utf-8')
            fromClient1 = fromClient1.split("\n")[0]
        
            print("Received from client: ", fromClient1, "\n")

        # with input_locks[1]:
        #     fromClient2 = connection.recv(1024).decode('utf-8')
        #     fromClient2 = fromClient2.split("\n")[0]
         
            # print("Received from client: ", fromClient2, "\n")
        # if not fromClient1 or not fromClient2:
            # break

        if not fromClient1:
            break

        if DEBUGMODE:
            print(fromClient1[-1], "\n")

        # assert type(fromClient1[-1]) == int
        if type(fromClient1[-1] == "\n"):
            print("FromClient", fromClient1)
            

        # if DEBUGMODE:
        #         print(fromClient2[-1], "\n")
        # assert type(fromClient2[-1]) == int

        # if fromClient1[-1] > fromClient2[-1]:
        #     fromClient =  fromClient2
        # elif fromClient2[-1] > fromClient1[-1]:
        #     fromClient =  fromClient1
        
        fromClient = fromClient1

        fromClient += "\n"
      
        if DEBUGMODE:
            print("Sending ", fromClient, "to client")
            inputList[1][0].send(fromClient.encode('utf-8'))
            inputList[0][0].send(fromClient.encode('utf-8'))

    connection.close()


while True:

    client, clientaddr = server.accept()

    if DEBUGMODE:
        print(f"Accepted connection from", clientaddr)

    inputList.append([client,clientaddr, len(inputList)])


    if DEBUGMODE:
        print("Sending client number: ", str(len(inputList)))

    toClient = client.send(str(len(inputList)).encode('utf-8'))
    
    with input_locks[0], input_locks[1]:

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