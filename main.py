import os
from controller import *

BUFFER_SIZE = 2048
# Set up HOST and PORT environmental variables before running
HOST_NAME = os.getenv("HOST")
PORT_NUMBER = int(os.getenv("PORT"))

controller = Controller(HOST_NAME, PORT_NUMBER)
controller.run_chat()
