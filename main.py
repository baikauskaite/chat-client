import os
import socket
from server_message import *

BUFFER_SIZE = 2048
HOST_NAME = os.getenv("HOST")
PORT_NUMBER = int(os.getenv("PORT"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST_NAME, PORT_NUMBER))

# First hand-shake message, encode it in bytes
buffer_str = "HELLO-FROM Viktorija\n"
buffer_bytes = buffer_str.encode()

# Send bytes to server
s.sendall(buffer_bytes)

# Receive bytes from server and decodes it
buffer_str = s.recv(BUFFER_SIZE)
decoded_str = buffer_str.decode()

# Parse the server message and respond accordingly
server_message = ServerMessage(decoded_str)
server_message.match_heading()

print(decoded_str)

s.close()
