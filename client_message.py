class ClientMessage:
    """ Contains methods to process user inputs and send them to the server """

    def __init__(self, socket):
        self.socket = socket

    # Private helper for sending messages
    def __send_message_to_server(self, text) -> None:
        message = text + "\n"
        message_bytes = message.encode("utf-8")
        self.socket.sendall(message_bytes)

    # Initiates a handshake with the server from the given user
    def first_handshake(self, username) -> None:
        self.__send_message_to_server("HELLO-FROM " + username)

    # Asks the server who is logged online
    def who(self) -> None:
        self.__send_message_to_server("WHO")

    # Tells the server to send the given message to the person with the given username
    def send_message(self, username, message):
        self.__send_message_to_server("SEND " + username + " " + message)
