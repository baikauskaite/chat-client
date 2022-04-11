import re
from server_message import *
from client_message import *


class Controller:
    """Interaction with the user, has a socket for sending and receiving messages from the server."""

    # Allows only 2-20 alphanumeric characters in username
    USERNAME_REGEX = "^[a-zA-Z0-9]{2,20}$"

    def __init__(self, socket):
        self.socket = socket
        self.client = ClientMessage(socket)

    # User manual that is displayed in the beginning and when called by writing '!help'
    def help(self) -> None:
        print("""
        @username message - to send a message to a user.        
        !who              - to list all users that are currently logged in.
        !quit             - to shutdown the client.
        !help             - to display the user manual
        """)

    # it wouldn't let me do self.server in the dictionary
    def return_users(self) -> None:
        self.client.who()
        server = ServerMessage(self.socket)
        server.who_ok()
        #self.interact_with_server(2)
        code = server.code
        if code in self.processes:
            self.processes[code](self)
        else:
            print("This should not get called.")

    # tells user program is quitting and quits
    def quit_program(self) -> None:
        self.socket.close()
        print("Quitting program.")
        quit()

    user_commands = {
        "!who": return_users,
        "!quit": quit_program,
        "!help": help
    }

    # parses what the user enters and begins the appropriate process
    # TODO: Add case for '@username message'
    def parse_user_input(self):
        user_input = input()
        if user_input[0] == "@":
            # separate username from body, remove @, process
            pass
        while user_input not in self.user_commands:
            user_input = input("There's no such command.")
        self.user_commands[user_input](self)

    # Prompts the user to select a username and initiates handshake with server
    def login(self) -> None:
        username = input("Please choose a username: ")
        while not re.match(self.USERNAME_REGEX, username):
            print("Your username should consist of 2-20 alphanumeric characters.")
            username = input("Please choose a username: ")
        self.client.first_handshake(username)
        server = ServerMessage(self.socket)
        server.second_handshake()
        code = server.code
        if code in self.processes:
            self.processes[code](self)
        else:
            print("This should not get called.")
        # self.interact_with_server(1)
        # self.client.first_handshake(username)

    # Refer to the class ServerMessage to see what each number refers to
    # Negative numbers indicate some kind of failure, positive indicate a successful process
    processes = {
        # too many clients in server
        -2: lambda x: print("Too many clients currently logged in. Try again later."),
        # username taken, login again
        -1: login,
        # successful command, user enter another command
        1: parse_user_input
    }

    """
    # Send client message and receive server message, continue the interaction with user according to server response
    # second parameter is a client method
    def interact_with_server(self, code_client_method_to_run):
        if code_client_method_to_run in self.client_method_to_run:
            self.client_method_to_run[code_client_method_to_run](self)
        else:
            print("This should not get called.")
        server = ServerMessage(socket)
        code = server.code
        # Calls a function corresponding to the code
        if code in self.processes:
            self.processes[code](self)
        else:
            print("This should not get called.")

    client_method_to_run = {
        1: self.client.first_handshake(username),
        2: self.server.who_ok()
    }
    """
