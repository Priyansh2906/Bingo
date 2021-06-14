import tkinter as tk
from tkinter import *
from tkinter import messagebox
import random
import socket
from socket import error
import threading
from PIL import ImageTk,Image
from time import sleep

#Establishing main client connection to the server
client_socket = socket.socket() #by default it is SOCK_STREAM (TCP) and has porotocal AF_INET (IPv4) 
client_socket.connect(('127.0.0.1',9999)) #server machine's ip and port on which it will send and recieve connections from

#Establishing player info transfer link to the server
player_info_socket = socket.socket() #by default it is SOCK_STREAM (TCP) and has porotocal AF_INET (IPv4)

player_connected = 0

while player_info_socket.connect_ex(("127.0.0.1",9998)) != 0:
    sleep(1) 

print("\n\nPlayer Socket connected to the server!!")
player_connected = int(str(player_info_socket.recv(2048).decode()))

#Essential variable declaration
linear_array = [i for i in range(1,26)]
random_array = []
removed_numbers=[]
number_to_send = None
num_to_recv = None
client_name = None
game_over = 0

def closeWindows():
    root.destroy()

################################# Creating startup window  ###################################
startup_menu = Tk()
startup_menu.title('Welcome to Bingo')
startup_menu.iconbitmap('icon.ico')
def storeName():
    global client_name
    client_name = getName.get('1.0',"end-1c")
    print("The player's name is : ",client_name)
    player_info_socket.send(bytes(client_name,"utf-8"))
    startup_menu.destroy()

#Startup Menu Frames
logo_frame = Frame(startup_menu)
logo_frame.pack(side=TOP,fill=X,pady=20)

startup_menu_center_frame = Frame(startup_menu)
startup_menu_center_frame.configure(background="light blue")
startup_menu_center_frame.pack(side=TOP,pady=20,padx=25)

how_to_play_frame = Frame(startup_menu)
how_to_play_frame.pack(side=TOP,pady=20)

how_to_play_frame_left = Frame(how_to_play_frame,width=50)
how_to_play_frame_left.pack(side=LEFT,padx=20)

how_to_play_frame_right = Frame(how_to_play_frame,width=50,relief="sunken")
how_to_play_frame_right.pack(side=TOP,padx=20)

lower_frame = Frame(startup_menu)
lower_frame.pack(side=TOP,pady=20)

logo = Label(logo_frame,text='B . I . N . G . O !!!',fg='red',bg='yellow',relief="sunken")
logo.configure(font=("cursive",30))
logo.pack(side=TOP,fill=X)

name_message = Label(startup_menu_center_frame,text="Enter your name to start playing : ")
name_message.configure(font=("courier",12))
name_message.pack(side=LEFT)
getName = Text(startup_menu_center_frame,height=1,width=25,bd=3,relief="groove")
getName.pack(side=RIGHT)

how_to_play = Label(how_to_play_frame_right,text="How to Play??",fg="red")
how_to_play.configure(font=("courier","20"))
how_to_play.pack(side=TOP)

grid_img = ImageTk.PhotoImage(Image.open("grid.png"))
grid_img_widget = Button(how_to_play_frame_left,image=grid_img,state="normal",relief="ridge")
grid_img_widget.pack()

step1 = Label(how_to_play_frame_right,text="> You get a 5x5 grid as shown.")
step1.configure(font=("courier",14))
step1.pack(side=TOP,pady=5)

step2 = Label(how_to_play_frame_right,text="> Click on a number to cross it.",fg="red")
step2.configure(font=("courier",14))
step2.pack(side=TOP,pady=5)

step3 = Label(how_to_play_frame_right,text="> If you cross a whole row,column ")
step3.configure(font=("courier",14))
step3.pack(side=TOP,pady=5)

step3_1 = Label(how_to_play_frame_right,text="or a diagonal fully , it will cross")
step3_1.configure(font=("courier",14))
step3_1.pack(side=TOP,pady=5)

step3_2 = Label(how_to_play_frame_right,text="one letter from word BINGO.")
step3_2.configure(font=("courier",14))
step3_2.pack(side=TOP,pady=5)

step4 = Label(how_to_play_frame_right,text="> Crossing all letters from Bingo",fg="red")
step4.configure(font=("courier",14))
step4.pack(side=TOP,pady=5)

step4_1 = Label(how_to_play_frame_right,text="makes you win the game!",fg="red")
step4_1.configure(font=("courier",14))
step4_1.pack(side=TOP,pady=5)

okBtn = Button(lower_frame,text="Play!!",command=storeName,height=2,width=20,bd=3,relief="ridge")
okBtn.pack(side=BOTTOM)
startup_menu.mainloop()
###################################################################################################

opponent_name = None
while opponent_name==None:
    opponent_name = player_info_socket.recv(4096).decode()
print("The opponent's name is : ",opponent_name)

####################  Creating Main Game window  #############################3
root = Tk()
root.title('Bingo!!')
root.iconbitmap('icon.ico')
#Creating Frames
frame1 = Frame(root)
frame1.pack(side=TOP,fill=X)

centerFrame = Frame(root)
centerFrame.pack(side=TOP)

frame2 = Frame(centerFrame)
frame2.pack(side=LEFT,fill=X,padx=10,pady=10)

opponent_info_frame = Frame(centerFrame)
opponent_info_frame.pack(side=TOP)

frame4 = Frame(centerFrame)
frame4.pack(side=RIGHT)

frame3 = Frame(root)
frame3.pack(side=TOP,fill=X,pady=5)

#Button click function
def numberClick(num,btn):
    global number_to_send
    #messagebox.showinfo('Message',str(num)+' is removed')
    number_to_send = num
    removed_numbers.append(num)
    btn.configure(text='X',fg="white")
    btn.configure(bg='red',fg='white')
    btn.configure(state="disabled")
    btn.configure(relief="sunken")
    print(removed_numbers)
    stmnt = str(num)+" was removed!!"
    
    textBox.configure(state="normal")
    textBox.delete('1.0', END)
    textBox.insert(END,stmnt)
    textBox.tag_add("center", 1.0, "end")
    textBox.configure(state="disabled")
    
    deleted_textbox.configure(state="normal")
    deleted_textbox.insert(END,str(num)+",")
    deleted_textbox.configure(state="disabled")
    
    turn_info.configure(state="normal",fg="red")
    turn_info.delete('1.0',END)
    turn_info.insert('1.0',"Opponent's Turn!!")
    turn_info.configure(state="disabled")
    
    victoryCondition()
    
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
    global opponent_name
    while True:
        msg = client_socket.recv(2048).decode()
        num_to_recv = int(msg) 
        button=button_mapping[num_to_recv]
        button.configure(text='X',fg="white")
        button.configure(bg='red',fg='white')
        button.configure(state="disabled")
        removed_numbers.append(num_to_recv)
        print(removed_numbers)
        stmnt = str(num_to_recv)+" was removed!!"
        textBox.delete('1.0', END)
        textBox.insert(END,stmnt)
        textBox.tag_add("center", 1.0, "end")
        deleted_textbox.configure(state="normal")
        deleted_textbox.insert(END,str(num_to_recv)+",")
        deleted_textbox.configure(state="disabled")
        
        turn_info.configure(state="normal",fg="green")
        turn_info.delete('1.0',END)
        turn_info.insert('1.0',"Your Turn!!")
        turn_info.configure(state="disabled")
        victoryCondition()

def winThread():
    won=player_info_socket.recv(1024).decode()
    won = int(won)
    if(won==1):
        messagebox.showinfo("Game over!!",opponent_name+" has won!!")
        game_over = 1 #Closes all windows
    if game_over==1:
        closeWindows()
    

def victoryCondition():
    global btns
    global game_over
    global B
    global I
    global N
    global G
    global O 
    victory_count = 0
    
    row_0 = 0
    row_1 = 0
    row_2 = 0
    row_3 = 0
    row_4 = 0
    
    col_0 = 0
    col_1 = 0
    col_2 = 0
    col_3 = 0
    col_4 = 0
    
    diag_1 = 0
    diag_2 = 0
    
    #Checking for rows
    if(btns[0][0]['state']=="disabled" and btns[0][1]['state']=="disabled" and btns[0][2]['state']=="disabled" and btns[0][3]['state']=="disabled" and btns[0][4]['state']=="disabled"):
        row_0 = 1
        victory_count+=1
        
    if(btns[1][0]['state']=="disabled" and btns[1][1]['state']=="disabled" and btns[1][2]['state']=="disabled" and btns[1][3]['state']=="disabled" and btns[1][4]['state']=="disabled"):
        row_1 = 1
        victory_count+=1
        
    if(btns[2][0]['state']=="disabled" and btns[2][1]['state']=="disabled" and btns[2][2]['state']=="disabled" and btns[2][3]['state']=="disabled" and btns[2][4]['state']=="disabled"):
        row_2 = 1
        victory_count+=1
        
    if(btns[3][0]['state']=="disabled" and btns[3][1]['state']=="disabled" and btns[3][2]['state']=="disabled" and btns[3][3]['state']=="disabled" and btns[3][4]['state']=="disabled"):
        row_3 = 1
        victory_count+=1
        
    if(btns[4][0]['state']=="disabled" and btns[4][1]['state']=="disabled" and btns[4][2]['state']=="disabled" and btns[4][3]['state']=="disabled" and btns[4][4]['state']=="disabled"):
        row_4 = 1
        victory_count+=1
    
    #Checking for coloums
    if(btns[0][0]['state']=="disabled" and btns[1][0]['state']=="disabled" and btns[2][0]['state']=="disabled" and btns[3][0]['state']=="disabled" and btns[4][0]['state']=="disabled"):
        col_0 = 1
        victory_count+=1
        
    if(btns[0][1]['state']=="disabled" and btns[1][1]['state']=="disabled" and btns[2][1]['state']=="disabled" and btns[3][1]['state']=="disabled" and btns[4][1]['state']=="disabled"):
        col_1 = 1
        victory_count+=1
        
    if(btns[0][2]['state']=="disabled" and btns[1][2]['state']=="disabled" and btns[2][2]['state']=="disabled" and btns[3][2]['state']=="disabled" and btns[4][2]['state']=="disabled"):
        col_2 = 1
        victory_count+=1
        
    if(btns[0][3]['state']=="disabled" and btns[1][3]['state']=="disabled" and btns[2][3]['state']=="disabled" and btns[3][3]['state']=="disabled" and btns[4][3]['state']=="disabled"):
        col_3 = 1
        victory_count+=1
        
    if(btns[0][4]['state']=="disabled" and btns[1][4]['state']=="disabled" and btns[2][4]['state']=="disabled" and btns[3][4]['state']=="disabled" and btns[4][4]['state']=="disabled"):
        col_4 = 1
        victory_count+=1  
    #Checking for diagonal (left to right)
    if(btns[0][0]['state']=="disabled" and btns[1][1]['state']=="disabled" and btns[2][2]['state']=="disabled" and btns[3][3]['state']=="disabled" and btns[4][4]['state']=="disabled"):
        diag_1=1
        victory_count+=1
        
    #Checking for diagonal (right to left)
    if(btns[0][4]['state']=="disabled" and btns[1][3]['state']=="disabled" and btns[2][2]['state']=="disabled" and btns[3][1]['state']=="disabled" and btns[4][0]['state']=="disabled"):
        diag_2=1
        victory_count+=1
    
    '''print("row 0 : ",row_0)
    print("row 1 : ",row_1)
    print("row 2 : ",row_2)
    print("row 3 : ",row_3)
    print("row 4 : ",row_4)
    
    print("col 0 : ",col_0)
    print("col 1 : ",col_1)
    print("col 2 : ",col_2)
    print("col 3 : ",col_3)
    print("col 4 : ",col_4)
    
    print("diag_1 : ",diag_1)
    print("diag_2 : ",diag_2)'''
    print("victory count : ",victory_count)
    if(victory_count>=1):
        B.configure(fg="red")
    if(victory_count>=2):
        I.configure(fg="red")
    if(victory_count>=3):
        N.configure(fg="red")
    if(victory_count>=4):
        G.configure(fg="red")
    if(victory_count>=5):
        O.configure(fg="red")
        player_info_socket.send(bytes("1","utf-8"))
        messagebox.showinfo('Winner!!',"You win!!!")       
        #game_over = 1 #Closes every window
        player_info_socket.close()
        client_socket.close()
        closeWindows()

#Functions and Threading definition part over. Now rendering main GUI

#Generating linear array and a random array from the linear array
for i in range(1,26):
    temp = random.choice(linear_array)
    linear_array.remove(temp)
    random_array.append(temp) 

#Generating Title bar
title = Label(frame1,text='B . I . N . G . O !!!',fg='red',bg='yellow',relief="sunken")
title.config(font=("Courier", 30))
title.pack(side=TOP,fill=X)

#Generating a 5x5 Button matrix
rows=5
columns=5
btns = [[None for i in range(rows)] for j in range(columns)]
button_mapping = {}
for i in range(rows):
    for j in range(columns):
        num = random.choice(random_array)
        random_array.remove(num)
        btns[i][j]=Button(frame2, text = num , fg ='red',height = 3, width = 5)
        btns[i][j]['command']=lambda btn=btns[i][j],num=num: numberClick(num,btn)
        btns[i][j]['borderwidth'] = 2
        btns[i][j]['relief'] = "groove"
        btns[i][j].grid(row=i,column=j)
        button_mapping[num]=btns[i][j]

#Printing numbers which are deleted 
textBox = Text(frame3, height = 1, width = 28)
textBox.tag_configure("center", justify='center')
textBox.insert("1.0","Recently Deleted Number")
textBox.tag_add("center", 1.0, "end")
textBox.pack(side=TOP)
textBox.configure(state="disabled")

#Displaying all removed numbers in a textbox
deleted_textbox = Text(frame4, height = 4, width = 28)
deleted_textbox.tag_configure("center", justify='center')
deleted_textbox.insert("1.0","Crossed Numbers : ")
deleted_textbox.tag_add("center", 1.0, "end")
deleted_textbox.pack(side=TOP,pady = 40)
deleted_textbox.configure(state="disabled")

#Displaying Bingo!
B = Label(frame4,text='B',fg='white',bg='light green',relief="sunken")
B.config(font=("cursive", 32))
B.pack(side=LEFT,padx=10)

I = Label(frame4,text='I',fg='white',bg='light green',relief="sunken")
I.config(font=("cursive", 32))
I.pack(side=LEFT,padx=10)

N = Label(frame4,text='N',fg='white',bg='light green',relief="sunken")
N.config(font=("cursive", 32))
N.pack(side=LEFT,padx=10)

G = Label(frame4,text='G',fg='white',bg='light green',relief="sunken")
G.config(font=("cursive", 32))
G.pack(side=LEFT,padx=10)

O = Label(frame4,text='O',fg='white',bg='light green',relief="sunken")
O.config(font=("cursive", 32))
O.pack(side=LEFT,padx=10)

#Displaying Player Names
opponent_name_textbox = Text(opponent_info_frame,height=2,width=20,fg="red")
opponent_name_textbox.insert('1.0',"Player : "+client_name+"\n")
opponent_name_textbox.insert("2.0","Opponent : "+opponent_name)
opponent_name_textbox.configure(state="disabled")
opponent_name_textbox.pack(side=TOP,pady=10)

#Displaying Whose turn is it
turn_info = Text(opponent_info_frame,height=1,width=20)
turn_info.insert('1.0',"Waiting to start..")
turn_info.configure(state="disabled")
turn_info.pack(side=TOP,pady=5)
#####################################################################################################

#Starting communication related threads
sending_thread = threading.Thread(target=sendMessage)
recieving_thread = threading.Thread(target=recieve)
winning_thread = threading.Thread(target=winThread)
sending_thread.start()
recieving_thread.start()
winning_thread.start()
root.mainloop()
print("Thank you for playing!! :)")