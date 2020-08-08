import socket
import threading
import requests
from bs4 import BeautifulSoup
import tkinter as tk
import sys
import os

ip_class = ['py-1']
#get the global ip address for the server
page = requests.get("https://www.whatismyip.com/")
page_soup = BeautifulSoup(page.text, 'html.parser')
ip_global = page_soup.select('.cf-footer-item')
ip_global = ip_global[1].text.split(' ')[-1]

# socket.AF_INET, socket.SOCK_STREAM
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''#works = leave blank and allow port through firewall and port forwarding to this port 25576
port = 25576
print(ip_global + ' : ' + str(port))
names = []
clients = []
server_socket.bind((host, port))
server_socket.listen(5)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
to_get_image = False


def broadcast(message):
    global clients
    for i in clients:
        try:
            i.send(bytes(message, 'utf-8'))
        except ConnectionResetError as e:
            pass

def get_image(size, client):
    print(size)
    client.recv(size)


def get_messages(name, client):
    client_msg = ''
    getting_image = False
    run = True
    print(f"new Thread has been created for {name}")
    while run:
        if to_get_image == False:
            try:
                client_msg = client.recv(1024).decode('utf-8')
            except:
                client_msg = ''

            msg_parts = client_msg.split(' ')
            print(client_msg[0:-1])
            if client_msg != '':
                if msg_parts[0] == 'SIZE':
                    image_dims = (int(msg_parts[1]), int(msg_parts[2]), int(msg_parts[3]))
                    image_size = msg_parts[4]
                    print(image_size)
                    broadcast('image')
                    print(msg_parts[1] + ' ' + msg_parts[2] + ' ' + msg_parts[3])
                elif client_msg == 'disconnect':
                    names.remove(name)
                    clients.remove(client)
                    print(name + ' has left the chat')
                    broadcast(name + ' has left the chat')
                    run = False
                    sys.exit(0)
                else:
                    print(name + ': ' + client_msg)
                    broadcast(name + ': ' + client_msg)




            # if message_split[0] == 'dev':
            #     get_server_details(message_split[1])


        # index = clients.index(client)



# def control_panel(command):
#     users = ''
#     print(command)
#     if command == 'users':
#         for i in names:
#             users += i + '\n'
#         return users
#     else:
#         return ''
#
#
# def control_panel_GUI():
#     panel = tk.Tk()
#     sizeX = 500
#     entry = tk.Entry(panel)
#     entry.pack()
#     text_box = tk.Text(panel)
#     send_button = tk.Button(panel, text='Send', command=lambda: text_box.insert('end', control_panel(entry.get())))
#     send_button.pack()
#     text_box.pack()
#     panel.mainloop()
#
# threading.Thread(target=control_panel_GUI()).start()





#listen for new connections
while True:
    client_socket, address = server_socket.accept()
    clients.append(client_socket)
    username = client_socket.recv(1024).decode('utf-8')
    names.append(username)
    print(f"connection from {address} has been made")
    print('Username: ' + username)
    client_socket.send(bytes("Ayo poop sock check!", 'utf-8'))
    broadcast(username + ' has joined the chat')
    print(username + ' has joined the chat')
    threading.Thread(target=get_messages, args=(username, client_socket)).start()


