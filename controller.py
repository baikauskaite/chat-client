import re
import sys

from server_message import *
from client_message import *
import threading


class Controller:
    """Interaction with the user, has a socket for sending and receiving messages from the server."""

    # Allows only 2-20 alphanumeric characters in username
    USERNAME_REGEX = "^[a-zA-Z0-9]{2,20}$"
    BUFFER_SIZE = 2048

    def __init__(self, socket):
        self.socket = socket
        self.client = ClientMessage(socket)
        self.server_messages_thread = threading.Thread(target=self.run_get_server_message, args=())
        self.server_messages_thread.daemon = True

    def run_chat(self):
        # TODO: The printing of !help in the beginning of program can be done here
        # TODO: Think of a way what to do if the user fails to log in (because BUSY or IN-USE)
        while not self.login():
            pass
        # Only start the thread for receiving server messages when the user has logged in
        # Do not continue to these lines until the user has logged in
        self.server_messages_thread.start()
        self.parse_user_input()

    # User manual that is displayed in the beginning and when called by writing '!help'
    def help(self) -> None:
        print("""
        @username message - to send a message to a user.        
        !who              - to list all users that are currently logged in.
        !quit             - to shutdown the client.
        !help             - to display the user manual
        """)

    # returns a list of all users online when user types "!who"
    def return_users(self) -> None:
        self.client.who()

    # tells user program is quitting and quits when user types "!quit"
    def quit_program(self) -> None:
        self.socket.close()
        print("Quitting program.")
        # TODO: Think of a better way to kill the thread before exiting
        sys.exit()

    user_commands = {
        "!who": return_users,
        "!quit": quit_program,
        "!help": help
    }

    # parses what the user enters and begins the appropriate process
    def parse_user_input(self):
        user_input = None
        while user_input != "!quit":
            # String user_input
            user_input = input()
            # boolean flag for loop
            recognized_command_entered = False

            while not recognized_command_entered:
                if user_input[0] == "@":
                    recognized_command_entered = True
                    username_and_message = self.get_username_and_message(user_input)
                    self.client.send_message(*username_and_message)
                    # TODO: program currently dies if username isn't recognized
                elif user_input in self.user_commands:
                    recognized_command_entered = True
                    self.user_commands[user_input](self)
                else:
                    user_input = input("There's no such command. Enter '!help' to see a list of valid commands.\n")

        self.quit_program()

    def get_username_and_message(self, user_input):
        user_and_message_list = user_input.split(' ', 1)
        username = user_and_message_list[0]
        username_no_at = username[1:]
        message = user_and_message_list[1]
        return (username_no_at, message)

    # Prompts the user to select a username and initiates handshake with server
    def login(self) -> bool:
        # have client select appropriate username
        username = self.get_username()
        # once username valid, connect to server with it
        self.client.first_handshake(username)
        # response will either be that username is taken, server is busy, login was successful, or bad request
        code = self.get_server_message()
        """ processing pauses when process_server_response is called so this doesn't work rn
        print(success)
        if success == 1:
            self.help()
        """
        return code == 1

    # Prompts the user to select a username and repeats the process until the username is good
    def get_username(self) -> str:
        username = input("Please choose a username: ")
        while not re.match(self.USERNAME_REGEX, username):
            print("Your username should consist of 2-20 alphanumeric characters.")
            username = input("Please choose a username: ")
        return username

    def run_get_server_message(self):
        while True:
            self.get_server_message()

    def get_server_message(self):
        byte_str = self.socket.recv(self.BUFFER_SIZE)
        if byte_str:
            server_message = ServerMessage(byte_str)
            code = server_message.code
            return code
