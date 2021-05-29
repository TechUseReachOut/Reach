import socket
import sys

HEADER = 64
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname()) #"192.168.X.X"
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def disconnect():
    send(DISCONNECT_MESSAGE)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT)) # LOG

def disconnect():
    send(DISCONNECT_MESSAGE)

def send_msg(msg='1', message=''): # msg_tag 1,2 or 3 - line number indicator of message string
    send(str(str(sys.argv[1]))+"||"+str(sys.argv[2]))

if str(sys.argv[1]) == "disconnect":
    disconnect()
else:
    send_msg()

