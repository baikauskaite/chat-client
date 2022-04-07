import os
import socket

BUFFER_SIZE = 2048
HOST_NAME = os.getenv("HOST")
PORT_NUMBER = int(os.getenv("PORT"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST_NAME, PORT_NUMBER))

# First hand-shake message
buffer_str = "HELLO-FROM Viktorija\n"
buffer_bytes = buffer_str.encode()

num_bytes_sent = s.send(buffer_bytes)
s.sendall(buffer_bytes)

buffer_str = s.recv(BUFFER_SIZE)
print(buffer_str)

s.close()
