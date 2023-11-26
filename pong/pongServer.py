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
sync_locks = [threading.Lock(), threading.Lock()]
syncs = [0,0]

# Initial Socket Setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Hosts and Ports
# host ="10.113.32.29"
host = "localhost"
port = 5001

# client and client address storage
inputList = []
# Mode for Debugging ( lessens printing in console)
DEBUGMODE = True
server.bind((host, port))
server.listen(2)

if DEBUGMODE:
    print(f"Server is listening on {host}:{port}")

def handle_client(connection, connectionAddress, otherClientsDict):

    # Purpose : to handle client threads

    # Main Client loop
    while True:
        #
        if DEBUGMODE:
            print("Looking for message from client")

        fromClient = connection.recv(1024).decode('utf-8')
        if not fromClient:
            break
        

        # Getting the first packet from what was recieved
        eos = fromClient.find("\n")
        fromClient = fromClient[:eos+1]

        print(fromClient[eos:])


        if DEBUGMODE:

            print("Left from Packet: ", fromClient[eos:])

            if fromClient[-1] == "\n":
                print("From Client: ", fromClient)
        
        send_otherClients(connectionAddress, fromClient, otherClientsDict)

    connection.close()


# =================================================================================================
    # Function : get_otherClients
    # Author : Taylor Payne
    # Purpose : To find other clients so that we 
    # do not send data back to the source client
# =================================================================================================

def get_otherClients(connectSock, connectAdd, otherClientsDict):

    otherClients = []

    for i in inputList:
        if connectSock != i[0] and connectAdd != i[1]:
            
            otherClients.append([i[0],i[1]])

    otherClientsDict[connectAdd] = otherClients
    

# =================================================================================================
    # Function : send_otherClients
    # Author : Taylor Payne
    # Purpose : Sends a payload 
    # To the other clients
# =================================================================================================
def send_otherClients(connectAdd, payload, otherClientsDict):

    for i in otherClientsDict[connectAdd]:

        if DEBUGMODE:
            print("Sending Payload!")

        # Sending payload to the socket of the other clients
        if payload.count("\n") == 1:
            i[0].send(payload.encode('utf-8'))
        else:
            print("Error: too many newlines")

while True:
    
    # Accepting new Connection
    client, clientaddr = server.accept()
    otherClientsDict = {}

    if DEBUGMODE:
        print(f"Accepted connection from", clientaddr)

    # Adding Connection to list of connections
    inputList.append([client,clientaddr])
    client.send(str(len(inputList)).encode('utf-8'))

    get_otherClients(client, clientaddr, otherClientsDict)
        
    # Starting Client Threads
    if len(inputList) == 2:
            
    
        client_handler = threading.Thread(target=handle_client, args=(client,clientaddr,otherClientsDict))
        client_handler1 = threading.Thread(target=handle_client, args=(client,clientaddr,otherClientsDict))

        client_handler.start()
        client_handler1.start()

        print(" Other Clients: ", otherClientsDict)


# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games