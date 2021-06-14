import random
import numpy as np
from colored import fg,bg,attr
from os import system, name
import socket
import time

def clear(): 

    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')

def deleteNum(grid,random_array,num):
    for i in range(0,25):
        if random_array[i]==num:
            random_array[i]='X'
    grid = np.array(random_array).reshape(5,5)

#Connection Part
client_socket = socket.socket() #by default it is SOCK_STREAM (TCP) and has porotocal AF_INET (IPv4) 
client_socket.connect(('127.0.0.1',9999)) #server machine's ip and port on which it will send and recieve connections from
print("Waiting for a match...may take a few seconds")
flag_client1=(client_socket.recv(1024).decode())
flag_client2=(client_socket.recv(1024).decode())
while(flag_client1=='0' and flag_client2=='0') or (flag_client1=='1' and flag_client2=='0') or (flag_client1=='0' and flag_client2=='1'):
    pass
    
#Game Logic
print("Match Found!! Game Session Started , Enjoy!!")
time.sleep(2)
clear()        
linear_array = [i for i in range(1,26)]
random_array = []
for i in range(1,26):
    temp = random.choice(linear_array)
    linear_array.remove(temp)
    random_array.append(temp)

grid = np.array(random_array).reshape(5,5)
for i in range(0,25):
        if i%5==0:
            print("\n")
        
        if random_array[i]=='X':
            print("\t",'%sX%s'%(fg(1),attr(0))," ",end="")
        else:
            print("\t",random_array[i]," ",end="")


#Deleting a number
while True:
    num = int(input("\n\nEnter a number to delete : "))
    deleteNum(grid,random_array,num)
    num_to_delete=client_socket.recv(1024).decode()
    #num_to_delete=int(num_to_delete)
    deleteNum(grid,random_array,num_to_delete)
    clear()
    client_socket.send(bytes(num))
    for i in range(0,25):
        if i%5==0:
            print("\n")
        
        if random_array[i]=='X':
            print("\t",'%sX%s'%(fg(1),attr(0))," ",end="")
        else:
            print("\t",random_array[i]," ",end="")     