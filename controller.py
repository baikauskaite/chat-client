import re
import socket
from server_message import *
from client_message import *
import threading


class Controller:
    """Interaction with the user, has a socket for sending and receiving messages from the server."""

    # Allows only 2-20 alphanumeric characters in username
    USERNAME_REGEX = "^[a-zA-Z0-9]{2,20}$"
    BUFFER_SIZE = 2048

    def __init__(self, host_name, port_number):
        self.host_name = host_name
        self.port_number = port_number

        self.socket = None
        self.client = None
        self.__initialize_socket()

        self.server_messages_thread = threading.Thread(target=self.run_get_server_message, args=())

    def __initialize_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host_name, self.port_number))
        self.socket = s
        self.client = ClientMessage(self.socket)

    # Responsible for the whole flow of the chat
    def run_chat(self):
        login_successful = self.login()
        while not login_successful == 1:
            if login_successful == -1:
                self.socket.close()
                self.__initialize_socket()
                login_successful = self.login()
            elif login_successful == -2:
                self.quit_program()
        self.help()
        # Only start the thread for receiving server messages when the user has logged in
        self.server_messages_thread.start()
        self.parse_user_input()
        self.quit_program()

    # User manual that is displayed in the beginning and when called by writing '!help'
    def help(self) -> None:
        print("""
        @username message - to send a message to a user.        
        !who              - to list all users that are currently logged in.
        !quit             - to shutdown the client.
        !help             - to display the user manual
        """)

    # Returns a list of all users online when user types "!who"
    def return_users(self) -> None:
        self.client.who()

    # Tells user program is quitting and quits when user types "!quit"
    def quit_program(self) -> None:
        # Closing the socket before killing the thread to raise an exception in run_get_server_message
        self.socket.close()
        self.server_messages_thread.join()
        print("Quitting program.")
        quit()

    user_commands = {
        "!who": return_users,
        "!quit": quit_program,
        "!help": help
    }

    # Parses what the user enters and begins the appropriate process
    def parse_user_input(self):
        user_input = None

        while user_input != "!quit":
            user_input = input()
            recognized_command_entered = False

            while not recognized_command_entered:
                if user_input[0] == "@":
                    recognized_command_entered = True
                    username_and_message = self.get_username_and_message(user_input)
                    self.client.send_message(*username_and_message)
                elif user_input in self.user_commands:
                    recognized_command_entered = True
                    self.user_commands[user_input](self)
                else:
                    user_input = input("There's no such command. Enter '!help' to see a list of valid commands.\n")

    # Extracts the username and message from the input and returns them in a tuple (username, message)
    def get_username_and_message(self, user_input):
        user_and_message_list = user_input.split(' ', 1)
        username = user_and_message_list[0]
        username_no_at = username[1:]
        message = user_and_message_list[1]
        return (username_no_at, message)

    # Prompts the user to select a username and initiates handshake with server
    def login(self) -> int:
        username = self.get_username()
        self.client.first_handshake(username)
        code = self.get_server_message()
        return code

    # Prompts the user to select a username and repeats the process until the username is good
    def get_username(self) -> str:
        username = input("Please choose a username: ")
        while not re.match(self.USERNAME_REGEX, username):
            print("Your username should consist of 2-20 alphanumeric characters.")
            username = input("Please choose a username: ")
        return username

    # Infinitely receives and processes server messages
    def run_get_server_message(self):
        while True:
            try:
                byte_str = self.socket.recv(self.BUFFER_SIZE)
            except OSError:
                # Catches the exception created by trying to recv from a closed socket
                break
            if byte_str:
                ServerMessage(byte_str)

    # Gets message from server and returns the code for success or error after processing the server message
    def get_server_message(self):
        byte_str = self.socket.recv(self.BUFFER_SIZE)
        if byte_str:
            server_message = ServerMessage(byte_str)
            code = server_message.code
            return code
