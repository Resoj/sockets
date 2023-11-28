# Contributing Authors:	    Taylor Payne Jose Cruz
# Email Addresses:          Thpa227@uky.edu Jcr242@uky.edu
# Date:                     Due on Nov 17
# Purpose:                  This Handles Data Processing between the Clients
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading




lPaddlePosy = 0
rpaddlePosy = 0

# Initial Socket Setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# Hosts and Ports
# host ="10.113.32.29"
host = "localhost"
port = 5050

# client and client address storage
inputList = {}

# Mode for Debugging ( lessens printing in console)
DEBUGMODE = True

server.bind((host, port))
server.listen(2)

if DEBUGMODE:
    print(f"Server is listening on {host}:{port}")





def handle_client(connection):

    # Purpose : to handle client threads

    # Main Client loop
    while True:
        #
        if DEBUGMODE:
            print("Looking for message from client")

        # Retrieving Client Game data 
        
        data = connection.recv(1024).decode('utf-8')
        
        paddlePosList = data.split("\n")[0]
        paddlePosList = paddlePosList.split(',')

        

        print("Paddle from Client: ", paddlePosList)
        if paddlePosList[2] == "l":
            print("sending to 2")
            inputList["right"][0].send(data.encode("utf-8"))
        elif paddlePosList[2] == "r": 
            print("sending to 1")
            inputList["left"][0].send(data.encode("utf-8"))

        


            

        
    connection.close()


while True:
    
    # Accepting new Connection
    client, clientaddr = server.accept()

    if DEBUGMODE:
        print(f"Accepted connection from", clientaddr)

    # Adding Connection to list of connections
    if len(inputList) == 0:
        inputList["left"] = [client, clientaddr]
        toClient = client.send(str(len(inputList)).encode('utf-8'))
        client_handler1 = threading.Thread(target=handle_client, args=(client,)) 

    elif len(inputList) == 1:
        inputList["right"] = [client, clientaddr]
        toClient = client.send(str(len(inputList)).encode('utf-8'))
        client_handler = threading.Thread(target=handle_client, args=(client,)) 
        

    if len(inputList) == 2:
        
        if DEBUGMODE:
            print("Starting Threads")

        client_handler.start()
        client_handler1.start()


# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games