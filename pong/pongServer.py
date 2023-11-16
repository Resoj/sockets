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
    # INITIAL MESSAGE FOR CLIENT NUMBER
    toClient = connection.send(str(len(inputList)).encode('utf-8'))
    
    while True:

        # Receive message from client
        fromClient = connection.recv(1024).decode('utf-8').split("\n")
        # print(len(fromClient.split(",")))

        fromClient = fromClient[0]

        print("received from client: ", fromClient)
        if not fromClient:
            break
        
        else:
            parsedData = fromClient.split(",")
            # PaddlePosL, PaddlePosR, ballPos, score, sync

            # Conncection 1
            if connection == inputList[0]:

                print(" \n Connection 1 is sending info")
                syncs[0] = int(parsedData[-1])
            # Conncection 2
            if connection == inputList[1]:

                print(" \n Connection 2 is sending info")
                syncs[1] = int(parsedData[-1])
            
            if syncs[0] == 0 and syncs[1] == 0:
                print("Both are zero")
            
            if syncs[0] > syncs[1]:
                # Update with data from connection 2
                print("Client 1 has a higher sync")
                inputList[1].sendall(fromClient[0].encode('utf-8'))
                

            if syncs[0] < syncs[1]:
                # Update with data from connection 1
                print("Client 2 has a higher sync")
                inputList[0].sendall(fromClient[0].encode('utf-8'))
                



        # for other_client in inputList:
        #         if other_client[0] != connection:
        #             print("sending: ", parsedData, " to ", other_client[1])
        #             other_client[0].send(parsedData.encode())
     
        # connection.send(fromClient.encode('utf-8'))
    connection.close()

ackCounter = 1
while True:

    client, clientaddr = server.accept()

    print(f"Accepted connection from", clientaddr)

    inputList.append([client,clientaddr, len(inputList)])

    print("Sending First ACK")

    client.send("ACK".encode('utf-8'))
    

    print("Waiting for HandShake")

    acknowledgment = client.recv(1024).decode('utf-8')

    if acknowledgment == "ACK":
        print("Received ACK", ackCounter)

        if ackCounter < 3:

            ackCounter += 1

    print("Sending Client Number")
    message = str(len(inputList)) + "\n"
    client.send(message.encode('utf-8'))

    if len(inputList) == 2:

        print("Starting Thread")

        client_handler = threading.Thread(target=handle_client, args=(client,clientaddr))

        client_handler.start()







# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games