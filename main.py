import os
import socket
import threading
from controller import *

BUFFER_SIZE = 2048
HOST_NAME = os.getenv("HOST")
PORT_NUMBER = int(os.getenv("PORT"))

controller = Controller(HOST_NAME, PORT_NUMBER)
# This function is responsible for the whole flow of the chat
controller.run_chat()
