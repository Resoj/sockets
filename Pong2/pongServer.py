# =================================================================================================
# Contributing Authors:	    Taylor Payne Jose Cruz
# Email Addresses:          Thpa227@uky.edu Jcr242@uky.edu
# Date:                     Due on Nov 17
# Purpose:                  This Handles Data Processing between the Clients
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading


# Lock Setup
input_locks = [threading.Lock(), threading.Lock()]
prevSeqNum = 0 

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
server.listen(2)

if DEBUGMODE:
    print(f"Server is listening on {host}:{port}")

def handle_client(connection, prevSeqNum):

    # Purpose : to handle client threads

    # Main Client loop
    while True:
        #
        if DEBUGMODE:
            print("Looking for message from client")

        # Retrieving Client Game data 
        with input_locks[0], input_locks[1]:
            
            fromClient = connection.recv(1024).decode('utf-8')

            fromClient = fromClient.split("\n")[0]
        
            print("Received from client: ", fromClient, "\n")

        # Break if there is no data 
        if not fromClient:
            break

        if DEBUGMODE:
                print("FromClient: ", fromClient)
                print("FromClient.split(): ", fromClient.split(','))
                print("FromClient.split()[0]: ", fromClient.split(',')[0])    

        seqNum= int(fromClient.split(',')[-2])

        fromClient += "\n"
        
        # if DEBUGMODE:
            # print("Sending ", fromClient, "to client")
    
        if seqNum >= prevSeqNum:
        
            if DEBUGMODE:
                print("Sending ", fromClient, "to client")

            inputList[1][0].send(fromClient.encode('utf-8'))
            inputList[0][0].send(fromClient.encode('utf-8'))
            if DEBUGMODE:
                print("Prev Sequence Number is now: ", seqNum)
                print(fromClient)
            prevSeqNum = int(fromClient[-2])

        

    connection.close()


while True:
    
    # Accepting new Connection
    client, clientaddr = server.accept()

    if DEBUGMODE:
        print(f"Accepted connection from", clientaddr)

    # Adding Connection to list of connections
    inputList.append([client,clientaddr, len(inputList)])


    if DEBUGMODE:
        print("Sending client number: ", str(len(inputList)))

    # Sending the Client its number ( 1 for left, 2 for right)
    toClient = client.send(str(len(inputList)).encode('utf-8'))
    
    # Starting Client Threads
    with input_locks[0], input_locks[1]:

        if len(inputList) == 1:

            if DEBUGMODE:
                print("Starting First Thread")

            client_handler1 = threading.Thread(target=handle_client, args=(client,prevSeqNum)) 

        if len(inputList) == 2:
            
            client_handler = threading.Thread(target=handle_client, args=(client,prevSeqNum))

            client_handler.start()
            client_handler1.start()


# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games