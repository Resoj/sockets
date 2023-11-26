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

def handle_client(connection, connectionAddress, connections):

    # Purpose : to handle client threads

    # Main Client loop
    while True:
        #
        if DEBUGMODE:
            print("Looking for message from client")

        # Retrieving Client Game data 
        with input_locks[0], input_locks[1]:
            
            fromClient1 = connection.recv(1024).decode('utf-8')

            fromClient1 = fromClient1.split("\n")[0]
        
            print("Received from client: ", fromClient1, "\n")

        # Break if there is no data 
        if not fromClient1:
            break
            
        fromClient = fromClient1

        fromClient += "\n"

        
      
        send_otherClients(connectionAddress, fromClient, connections)
        

    connection.close()




# =================================================================================================
    # Function : get_otherClients
    # Author : Taylor Payne
    # Purpose : To find other clients so that we 
    # do not send data back to the source client
# =================================================================================================

def get_otherClients(connectSock, connectAdd, otherClientsDict, inputList):


    otherClients = []

    for i in inputList:
        if i[0] != connectSock and i[1]!= connectAdd:
            otherClients.append([i[0], i[1], i[2]])

    if len(otherClients) > 0:
        print("Other Clients found: ", otherClients)
        otherClientsDict[connectAdd] = otherClients
    else:
        print("No other Clients found")


# =================================================================================================
    # Function : send_otherClients
    # Author : Taylor Payne
    # Purpose : Sends a payload 
    # To the other clients
# =================================================================================================

def send_otherClients(connectAdd, payload, otherClientsDict):

    if otherClientsDict[connectAdd] == None:
        print(" No other Clients to send to")
        return

    for i in otherClientsDict[connectAdd]:

       

        # Sending payload to the socket of the other clients
        if payload.count("\n") == 1:

            if DEBUGMODE:
                print("Sending Payload to ", otherClientsDict[connectAdd][i])
        
            i[0].send(payload.encode('utf-8'))

        else:
            print("Error: too many newlines")




while True:
    
    # Accepting new Connection
    client, clientaddr = server.accept()

    if DEBUGMODE:
        print(f"Accepted connection from", clientaddr)

    # Adding Connection to list of connections
    inputList.append([client,clientaddr, len(inputList)])

    if DEBUGMODE:
        print("INPUT LIST: ", inputList, "\n")
    

    clients = {}


    if DEBUGMODE:
        print("Sending client number: ", str(len(inputList)))

    # Sending the Client its number ( 1 for left, 2 for right)
    toClient = client.send(str(len(inputList)).encode('utf-8'))


    if len(inputList) == 2:        

        client_handler1 = threading.Thread(target=handle_client, args=(client,clientaddr, clients))

        if client == inputList[0][0]:
            get_otherClients(inputList[0][0], inputList[0][1], clients, inputList)

        client_handler2 = threading.Thread(target=handle_client, args=(client,clientaddr, clients))

            
        if client == inputList[1][0]:
            get_otherClients(inputList[1][0], inputList[1][1], clients, inputList)

        client_handler1.start()
        client_handler2.start()

           

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games