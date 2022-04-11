class ServerMessage:
    """Server message is split to head and body. The body can then processed according to the heading."""

    BUFFER_SIZE = 2048

    # Splitting the message into a heading and a body
    def __init__(self, socket):
        self.socket = socket
        self.head = None
        self.body = None
        # code defines the next action for the controller to take
        self.code = self.receive_server_message()

    # Receive a message from the server and determine what kind of message it is
    def receive_server_message(self) -> int:
        # Receive bytes from server and decode it
        buffer_str = self.socket.recv(self.BUFFER_SIZE)
        decoded_str = buffer_str.decode()
        # Parse the server message and respond accordingly
        self.split_message(decoded_str)
        code = self.match_heading()
        return code

    # Split server message to head and body
    def split_message(self, message):
        # Remove the trailing newline and split the message
        message = message.rstrip()
        word_list = message.split()
        self.head = word_list.pop(0)
        self.body = word_list

    # Server's response to a correct first-handshake
    # Returns a code which can be used by the controller to determine that there was no failure in the process
    def second_handshake(self) -> int:
        username = self.body[0]
        print("You have successfully logged in, " + username + ".")
        return 1

    def send_ok(self) -> int:
        print("The message has been sent successfully.")
        return 1

    def unknown(self) -> int:
        print("The user you're trying to message is currently not logged in.")
        return 1

    # TODO: I'm thinking the parsing and printing of the message should take place in the controller, since
    # server_message shouldn't care about formatting anything?
    # that would impact the whole return int code though
    # let's just get it to work fully first, then maybe refactor things
    def delivery(self) -> int:
        username = self.body.pop(0)
        message = self.body
        print([username] + [": "] + message)
        return 1

    def in_use(self) -> int:
        print("This username is already in use.")
        return -1

    def busy(self) -> int:
        print("The maximum number of users are currently using the chat.")
        return -2

    def who_ok(self) -> int:
        list_of_names = self.body # .split()
        print("Users currently online:\n")
        for name in list_of_names:
            print(name + "\n")
        return 1

    # TODO: maybe have this throw an exception, since the user shouldn't be worried about headers
    def bad_rqst_hdr(self) -> int:
        print("Error in request header, please try again.")
        return 1

    def bad_rqst_body(self) -> int:
        print("Error in message body, please try again.")
        return 1

    # Pairs of headings and functions to process the body for the matching heading
    headings = {
        "HELLO": second_handshake,
        "SEND-OK": send_ok,
        "UNKNOWN": unknown,
        "DELIVERY": delivery,
        "IN-USE": in_use,
        "BUSY": busy,
        "WHO-OK": who_ok,
        "BAD-RQST-HDR": bad_rqst_hdr,
        "BAD-RQST-BODY": bad_rqst_body
    }

    # Match heading with a function to process the message's body
    # TODO: else case, when there's no matching heading in headings
    def match_heading(self) -> int:
        if self.head in self.headings:
            return self.headings[self.head](self)
        else:
            print("This code is not yet implemented.")
            return 0