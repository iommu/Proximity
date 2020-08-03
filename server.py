import socket
import threading
import os
from sys import platform
import base64
from colorama import init
import colorama
from pyfiglet import figlet_format
from termcolor import cprint
import sys
from subprocess import check_output
import time
import queue

if platform == "linux" or platform == "linux2":
    os.system('clear')
    if (os.path.exists('ip.txt')):
        os.remove('ip.txt')
    os.system("ifconfig | grep 192 | awk -F ' ' '{print $2}' > ip.txt")
    f = open('ip.txt', 'r')
    line = f.readline()
    os.remove('ip.txt')
    SERVER = line.strip()
elif platform == "win32":
    os.system('cls')
    SERVER = socket.gethostbyname(socket.gethostname())
else:
    print('Unsupported OS')
    exit(1)

colorama.init()
cprint(figlet_format('PROXIMITY', font="standard"), "cyan")

PORT = 5050


def print_to_stdout(*a):
    print(*a, file=sys.stdout)


def encodefunc(val):
    encoded_data = base64.b64encode(bytes(val, 'utf-8'))
    print(
        f"\n\n-------- {username}'s Chat-Room accesskey : ( {encoded_data.decode('utf-8')} ) --------")


def getpasskey(str1):
    if str1[0:7] == '192.168':
        encodefunc(str1[7:].zfill(8))
    else:
        encodefunc(str1.zfill(15))

no_client = 1
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

HEADER = 64
DISCONNECT_MESSAGE = "exit"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(ADDR)
except:
    print('A room already exists in this server')
    exit(1)

cache_msg = queue.Queue()

def readinput():
    global user_input
    user_input = input()
    
    cache_msg.put(user_input)
    return


userinput = threading.Thread(target=readinput, args=())
connection_cl = 0


def handle_client(conn, addr):
    try:
        global no_client
        
        global userinput
        global connection_cl
        uname = conn.recv(10).decode(FORMAT)
        
        print(f"{uname} joined the chat")
        no_client = 0

        
        while(True):
            message_length = conn.recv(HEADER).decode(FORMAT)
            message_length = int(message_length)
            message_rec = conn.recv(message_length).decode(FORMAT)
            if message_rec == DISCONNECT_MESSAGE:
                print(f'{uname} left the chat')
                no_client = 1
                connection_cl = 1
                userinput.join()
                
                break
            print(f"\t\t\t\t\t\t{uname} > {message_rec}")
        conn.close()
        
    except (ConnectionResetError, ConnectionAbortedError,OSError):
        pass


user_input = ''
message_val = ''

if user_input == DISCONNECT_MESSAGE:
        os._exit(0)

def send_message(conn, addr):
    conn.send(username.encode(FORMAT))
    global userinput
    global connection_cl
    global message_val
    global cache_msg
    global no_client
    cache_msg.queue.clear()
    
    while(conn.fileno()):
        
        if (not userinput.is_alive()):
            global user_input
            
            if user_input != '':
                
                if no_client == 1:
                    
                    cache_msg.queue.clear()
                    empty_str = ''
                    cache_msg.put(empty_str)        
                
                
                message_val = cache_msg.get()
                
                another = message_val
            user_input = ''
            
            userinput = threading.Thread(target=readinput, args=())
            userinput.start()
        if message_val != '' :
            

            if no_client == 0:
                
                message = message_val.encode(FORMAT)
                message_val = ''
                message_length = len(message)
                send_len = str(message_length).encode(FORMAT)
                send_len += b' '*(HEADER-len(send_len))
                try:
                    conn.send(send_len)
                    conn.send(message)
                    if another == DISCONNECT_MESSAGE:
                        conn.close()
                        cache_msg.queue.clear()
                        os._exit(0)
                except:
                    
                    pass
        if connection_cl == 1:
            connection_cl = 0
            conn.close()
            cache_msg.queue.clear()
            return
    conn.close()
    os._exit(0)


def start_sockets():
    server.listen()
    while(1):
        conn, addr = server.accept()
        client_thread = threading.Thread(
            target=handle_client, args=(conn, addr))
        send_thread = threading.Thread(target=send_message, args=(conn, addr))
        client_thread.start()
        send_thread.start()
        print(f"\n[ACTIVE CONNECTIONS] {threading.activeCount()-1}")


print('Starting server...\n')
username = input('Enter your username : ')
getpasskey(SERVER)
start_sockets()
