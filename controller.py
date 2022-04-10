import re
from server_message import *


class Controller:
    """Interaction with the user, has a socket for sending and receiving messages from the server."""

    # Allows only 2-20 alphanumeric characters in username
    USERNAME_REGEX = "^[a-zA-Z0-9]{2,20}$"

    def __init__(self, socket):
        self.socket = socket

    # Prompts the user to select a username and initiates handshake with server
    def login(self):
        username = input("Please choose a username: ")
        while not re.match(self.USERNAME_REGEX, username):
            print("Your username should consist of 2-20 alphanumeric characters.")
            username = input("Please choose a username: ")
        # TODO: Change the string below in the brackets to a ClientMessage object
        self.interact_with_server("HELLO-FROM " + username + "\n")

    # Send client message and receive server message, continue the interaction with user according to server response
    def interact_with_server(self, message):
        self.send_client_message(message)
        server_message = ServerMessage(self.socket)
        code = server_message.code
        # Calls a function corresponding to the code
        if code in self.processes:
            self.processes[code]()
        else:
            print("This code is not yet implemented.")

    # Refer to the class ServerMessage to see what each number refers to
    processes = {
        -1: login
    }

    # Encode a message and send it to the server
    # TODO: This should be a method of ClientMessage class
    def send_client_message(self, message):
        message_bytes = message.encode()
        self.socket.sendall(message_bytes)
