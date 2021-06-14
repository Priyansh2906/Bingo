import socket
import threading

def sendClient1():
    while True:
        msg = c1.recv(4096)
        if(msg!=None):
            print(msg)
            msg = msg.decode()
            c2.send(bytes(msg,"utf-8"))

def sendClient2():
    while True:
        msg = c2.recv(4096)
        if(msg!=None):
            print(msg)
            msg = msg.decode()
            c1.send(bytes(msg,"utf-8"))

def player1_nameThread():
    while True:
        name = p1.recv(4096)
        if(name!=None):
            print("Player 1's name is : ",name)
            name = name.decode()
            p2.send(bytes(name,"utf-8"))
            print("Name sent to player 2")
            break

def player1_winThread():
    while True:
        win = p1.recv(1024)
        if(win!=None):
            print("Player 1 has won!!")
            win=win.decode()
            p2.send(bytes(win,"utf-8"))
            break

def player2_nameThread():
    while True:
        name = p2.recv(4096)
        if(name!=None):
            print("Player 2's name is : ",name)
            name = name.decode()
            p1.send(bytes(name,"utf-8"))
            print("Name sent to player 1")
            break

def player2_winThread():
    while True:
        win = p2.recv(1024)
        if(win!=None):
            print("Player 2 has won!!")
            win=win.decode()
            p1.send(bytes(win,"utf-8"))
            break
#Socket variables for main client to client communication   

c1 = None #Client socket1
addr1 = None #Client address1
c2 = None #Client socket2
addr2 = None #Client address2	


#Socket variables for Player Info
p1 = None #Player_info socket1
p_addr1 = None #Player1 address
p2 = None #Player_info socket1
p_addr2 = None #Player1 address

#Connecting Main clients first for main game communication
server_socket1 = socket.socket() #by default it is SOCK_STREAM (TCP) and has porotocal AF_INET (IPv4) 
server_socket1.bind(('127.0.0.1',9999)) #server machine's ip and port on which it will send and recieve connections from
server_socket1.listen(2) #We will only accept two connections as of now , one for each client
print("Server started successfully!!!")
print("Waiting for connections...\n\n")

while (((c1 is None)and(addr1 is None)) and ((c2 is None) and (addr2 is None))):
        
    if((c1 is None) and (addr1 is None)):
        c1,addr1 = server_socket1.accept()
        print("User connected to client1 socket!!")   

    if((c2 is None) and (addr2 is None)):
        c2,addr2 = server_socket1.accept()
        print("\n\nUser connected to client2 socket!!")

#Now connecting player sockets to server to transfer player info of the current session
player_socket1 = socket.socket() #by default it is SOCK_STREAM (TCP) and has porotocal AF_INET (IPv4) 
player_socket1.bind(('127.0.0.1',9998)) #server machine's ip and port on which it will send and recieve connections from
player_socket1.listen(2) #We will only accept two connections as of now , one for each client
print("Both clients connected successfully!")
print("Now transferring player info...\n\n")

player_1_name = ""
player_2_name = ""

while (((p1 is None)and(p_addr1 is None)) and ((p2 is None) and (p_addr2 is None))):
        
    if((p1 is None) and (p_addr1 is None)):
        p1,p_addr1 = player_socket1.accept()
        p1.send(bytes("1","utf-8"))
        p1.send(bytes(player_2_name,"utf-8"))
        print("Player1 Info transfer link established!!")   

    if((p2 is None) and (p_addr2 is None)):
        p2,p_addr2 = player_socket1.accept()
        p2.send(bytes("1","utf-8"))
        
        print("\n\nPlayer2 Info transfer link established!!")

#Initialising threads and starting them
send_to_client1 = threading.Thread(target=sendClient1)
send_to_client2 = threading.Thread(target=sendClient2)
send_to_client1.start()
send_to_client2.start()

p1_thread = threading.Thread(target=player1_nameThread)
p2_thread = threading.Thread(target=player2_nameThread)
p1_thread.start()
p2_thread.start()

p1_win = threading.Thread(target=player1_winThread)
p2_win = threading.Thread(target=player2_winThread)
p1_win.start()
p2_win.start()