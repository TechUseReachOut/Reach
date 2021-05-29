import socket
import threading

HEADER = 64
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname()) #"192.168.X.X"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

msg_queue = []
msg_tag, message = '',''            
def queue_msg(msg_tag, message):
    msg_tag, message = msg_tag, message
    return msg_tag, message

def send_this():
    this = msg_queue.pop(0)
    return this

def handle_client(conn, addr, msg_queue):
    print(f"{addr} connected") # LOG
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) 
        if msg_length:

            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"{addr} disconnected") # LOG
                conn.send("DISCONNECTED".encode(FORMAT))
            elif msg =="a":
                print(f"{addr} : {msg} - camera") # LOG
                if not msg_queue == []:
                    this = send_this() 
                    conn.send(this.encode(FORMAT))
                else:
                    conn.send("no update".encode(FORMAT))
            else:
                print(f"{addr} : {msg} - client") # LOG
                msg_queue += [msg]
                conn.send(f"received {msg}".encode(FORMAT))
        else:
            #print(f"{addr} : {msg} - no update") # LOG
            conn.send("no update".encode(FORMAT))
    conn.close()

def start():
    server.listen()
    print(f"Listening {server}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr,msg_queue))
        thread.start()
        print(f"Active {threading.activeCount() -1}") # MONITOR
    
print("starting...") # MARKER
start()


