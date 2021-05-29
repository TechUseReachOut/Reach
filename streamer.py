import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import socket
import pyvirtualcam

def overlay_change(frame):
    overlay_box_ = './images/overlay_box.png'
    overlay_rect_ = './images/overlay_rect.png'
    return overlay_box_,overlay_rect_

def send(msg_):
    message = msg_.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    msg = str(client.recv(2048).decode(FORMAT))
    return msg

update_flag = True#False
vc = cv2.VideoCapture(0)

overlay = None
b,g,r,a = 0,0,0,0
msg = ["NEWS DEVELOPMENT","NAGBITIW NA SA PWESTO AND QUEEN","BEE DAHIL SA PAGNANAKAW NG TAO","SA KANILANG HONEY"]
fontpath = "./fonts/Helvetica-Bold.ttf"
font = ImageFont.truetype(fontpath, 32)

HEADER = 64 # allowed length of message in bytes
PORT = 8080
SERVER = "192.168.100.24" # socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

update = ''
command = ''
interval = 0
delay = 10
video = vc
width= int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer= cv2.VideoWriter('recording.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))

with pyvirtualcam.Camera(width=640, height=480, fps=30) as cam:
    while command !='stop':
        if interval >= delay:
            update = send("a")# sending message
            interval = 0
            if '||' in update:
                print("!message update") # LOG
                tag,message = str(update).split("||")
                msg[int(tag)] = message
        else:
            interval += 1

        rval, frame = vc.read()
        frame = cv2.flip(frame,1)
        if update_flag:
            overlay_box_, overlay_rect_ = overlay_change(frame)
            update_flag = False

        if any(overlay_box_):
            overlay_box = cv2.imread(f'{overlay_box_}')
            frame[350:472,4:202] = overlay_box
        if any(overlay_rect_):
            overlay_rect = cv2.imread(f'{overlay_rect_}')
            frame[376:491,4:635] = overlay_rect

        img_pil = Image.fromarray(frame)

        if any(msg):
            draw = ImageDraw.Draw(img_pil)

        if msg[1]:
            draw.text((8, 380), msg[1], font = font, fill = (b, g, r, a))
        if msg[2]:
            draw.text((8, 415), msg[2], font = font, fill = (b, g, r, a))
        if msg[3]:
            draw.text((8, 450), msg[3], font = font, fill = (b, g, r, a))
        img = np.array(img_pil)

        cv2.imshow("Streaming", img)
        writer.write(img)

        cam.send(img)
        cam.sleep_until_next_frame()
        cam.sleep_until_next_frame()

        if not vc.isOpened():
            msgBox = QMessageBox()
            msgBox.setText("Failed to open camera.")
            msgBox.exec_()
        cv2.waitKey(1)

vc.release()
writer.realease()
cv2.destroyAllWindows()







