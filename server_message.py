class ServerMessage:
    """Server message is split to head and body. The body can then processed according to the heading."""

    # Splitting the message into a heading and a body
    def __init__(self, message):
        word_list = message.split()
        self.head = word_list.pop(0)
        self.body = word_list

    # Server's response to a correct first-handshake
    # Returns a code which can be used by the controller to determine that there was not failure in the process
    # TODO: There's an error in the concatenation
    # TODO: newlines should be removed from the request's body
    def second_handshake(self) -> int:
        username = self.body[0]
        print("You have successfully logged in, " + username + ".")
        return 1

    def send_ok(self) -> int:
        print("The message has been sent successfully.")
        return 2

    def unknown(self) -> int:
        print("This user is currently not logged in.")
        return -3

    def delivery(self) -> int:
        username = self.body[0]
        message = self.body[1]
        print(username + ": " + message)
        return 2

    def in_use(self) -> int:
        print("This username is already in use.")
        return -1

    def busy(self) -> int:
        print()
        return -2

    # Pairs of headings and functions to process the body for the matching heading
    headings = {
        "HELLO": second_handshake,
        "SEND-OK": send_ok,
        "UNKNOWN": unknown,
        "DELIVERY": delivery,
        "IN-USE": in_use,
        "BUSY": busy
    }

    # Match heading with a function to process the message's body
    # TODO: else case, when there's no matching heading in headings
    def match_heading(self) -> int:
        function = self.headings[self.head]
        if function is not None:
            return function(self)
        else:
            pass