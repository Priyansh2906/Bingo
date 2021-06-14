import tkinter as tk
from tkinter import *
from tkinter import messagebox
import random
import socket
import threading

'''#Connection Part
client_socket = socket.socket() #by default it is SOCK_STREAM (TCP) and has porotocal AF_INET (IPv4) 
client_socket.connect(('127.0.0.1',9999)) #server machine's ip and port on which it will send and recieve connections from'''

root = Tk()
linear_array = [i for i in range(1,26)]
random_array = []
removed_numbers=[]
number_to_send = None
num_to_recv = None

#Button click function
def numberClick(num,btn):
    global number_to_send
    #messagebox.showinfo('Message',str(num)+' is removed')
    number_to_send = num
    removed_numbers.append(num)
    btn.configure(text='X')
    btn.configure(bg='red',fg='white')
    btn.configure(state="disabled")
    print(removed_numbers)

#Message Sending and recieving threads that manages communication
def sendMessage():
    global number_to_send
    while True:
        if number_to_send!=None:
            number_to_send = str(number_to_send)
            client_socket.send(bytes(number_to_send,"utf-8"))
            number_to_send = None

def recieve():
    global num_to_recv
    global button_mapping
    global removed_numbers
    while True:
        msg = client_socket.recv(2048).decode()
        num_to_recv = int(msg) 
        button=button_mapping[num_to_recv]
        button.configure(text='X')
        button.configure(bg='red',fg='white')
        button.configure(state="disabled")
        removed_numbers.append(num_to_recv)
        print(removed_numbers)

#root.geometry("200x200") 
#Generating linear array and a random array from the linear array
for i in range(1,26):
    temp = random.choice(linear_array)
    linear_array.remove(temp)
    random_array.append(temp) 

#Generating a 5x5 Button matrix
rows=5
columns=5
btns = [[None for i in range(rows)] for j in range(columns)]
button_mapping = {}
for i in range(rows):
    for j in range(columns):
        num = random.choice(random_array)
        random_array.remove(num)
        btns[i][j]=Button(root, text = num , fg ='red',height = 3, width = 5)
        btns[i][j]['command']=lambda btn=btns[i][j],num=num: numberClick(num,btn)
        btns[i][j].grid(row=i,column=j)
        button_mapping[num]=btns[i][j]

sending_thread = threading.Thread(target=sendMessage)
recieving_thread = threading.Thread(target=recieve)
sending_thread.start()
recieving_thread.start() 
root.mainloop()