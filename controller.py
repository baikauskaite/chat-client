import re
from server_message import *


class Controller:
    """Interaction with the user, has a socket for sending and receiving messages from the server."""

    BUFFER_SIZE = 2048
    USERNAME_REGEX = "^[a-zA-Z0-9]{2,20}$"

    def __init__(self, socket):
        self.socket = socket

    def login(self):
        username = input("Please choose a username: ")
        while not re.match(self.USERNAME_REGEX, username):
            print("Your username should consist of 2-20 alphanumeric characters.")
            username = input("Please choose a username: ")
        # TODO: Change the string below in the brackets to a ClientMessage object
        self.interact_with_server("HELLO-FROM " + username)

    # Send client message and receive server message, continue the interaction with user according to server response
    def interact_with_server(self, message):
        self.send_client_message(message)
        code = self.receive_server_message()
        # Calls a function corresponding to the code
        function = self.processes[code]
        if function is not None:
            function()
        else:
            print("This code is not yet implemented")

    # Refer to the class ServerMessage to see what each number refers to
    processes = {
        -1: login
    }

    # Encode a message and send it to the server
    def send_client_message(self, message):
        message_bytes = message.encode()
        self.socket.sendall(message_bytes)

    # Receive a message from the server and determine what kind of message it is
    def receive_server_message(self) -> int:
        # Receive bytes from server and decode it
        buffer_str = self.socket.recv(self.BUFFER_SIZE)
        decoded_str = buffer_str.decode()
        # Parse the server message and respond accordingly
        server_message = ServerMessage(decoded_str)
        code = server_message.match_heading()
        return code
