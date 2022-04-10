import os
import socket
from controller import *

BUFFER_SIZE = 2048
HOST_NAME = os.getenv("HOST")
PORT_NUMBER = int(os.getenv("PORT"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST_NAME, PORT_NUMBER))

controller = Controller(s)
controller.help()
controller.login()

s.close()
