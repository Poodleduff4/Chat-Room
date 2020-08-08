import socket
import tkinter as tk
from tkinter import filedialog
import threading
import sys
import winsound
import os
from PIL import Image
import cv2
import numpy as np


# socket.AF_INET, socket.SOCK_STREAM
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# address = socket.gethostname()#if on different machines put the ip of the server here
home_ip = '127.0.0.1'
address = str(input("Enter the ip"))#works = use the ipv4 address of the server host and allow port through firewall
port = 25576#port of the server stays the same
username = bytes(input('Enter your username: '), 'utf-8')
try:
    s.connect((address, port))
    print(f'connected to {address}')
except:
    print('could not connect to server, Retrying with home ip...')
    try:
        s.connect((home_ip, port))
        print(f'connected to {home_ip}')
    except:
        print('Could not connect to anything, Exiting the client...')
        sys.exit(0)
s.send(username)
msg = s.recv(1024)
print(msg.decode('utf-8'))


def send_message():
    s.send(bytes(entry.get(), 'utf-8'))
    entry.delete(0, 'end')

def send_image():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("png",
                                                      "*.png*"),
                                                     ("jpg",
                                                      "*.jpg*")))

    # Change label contents
    label_file_explorer.configure(text="File Opened: " + filename)
    image_data = cv2.imread(filename)
    #send data
    shape = image_data.shape
    print(shape)
    arr = np.array(image_data)
    arrString: bytes = arr.tobytes()
    image_size = os.path.getsize(filename)
    print(image_size)

    s.send(bytes(f"SIZE {shape[0]} {shape[1]} {shape[2]} {image_size} {arrString}", 'utf-8'))

    #show image
    # cv2.imshow(filename.split('/')[-1], image_data)
    # k = cv2.waitKey(0)
    # if k == 32:
    #     cv2.destroyAllWindows()



def receive_messages():
    message = ''
    while True:
        try:
            message = s.recv(1024).decode('utf-8')
            winsound.MessageBeep(-1)
            print(message)
            chat.insert('end', message + '\n')
            chat.see("end")
        except ConnectionAbortedError:
            print("You have left the chat")
            os._exit(0)

panel = tk.Tk()
sizeX = 500
sizeY = 500
panel.title('pisschat')
frame = tk.Frame(panel, width=sizeX, height=sizeY)
frame.pack()
entry = tk.Entry(frame)
entry.pack(side=tk.LEFT)
send = tk.Button(frame, text='Send', command=send_message)
send.pack(side=tk.RIGHT)
image_button = tk.Button(panel, text='Image', command=send_image)
image_button.pack()
label_file_explorer = tk.Label(panel,  text="File Explorer using Tkinter", width=100, height=4, fg="blue")
label_file_explorer.pack()
scrollbar = tk.Scrollbar(panel)
scrollbar.pack(side='right', fill='y')
chat = tk.Text(panel, yscrollcommand=scrollbar.set)
chat.pack()
scrollbar.config(command=chat.yview)
def on_closing():
    s.send(bytes('disconnect', 'utf-8'))
    s.close()
    panel.destroy()
    os._exit(0)

panel.protocol("WM_DELETE_WINDOW", on_closing)
threading.Thread(target=receive_messages).start()
panel.mainloop()
