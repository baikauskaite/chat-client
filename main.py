import os
import socket
import threading
from controller import *

BUFFER_SIZE = 2048
HOST_NAME = os.getenv("HOST")
PORT_NUMBER = int(os.getenv("PORT"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST_NAME, PORT_NUMBER))

controller = Controller(s)
# moving to login so that the user only knows how to interact if they successfully logged in
# controller.help()
is_success = controller.login()
if is_success:
    t = threading.Thread(target=controller.getting_server_message, args=(s,))
    t.start()
    controller.parse_user_input()
