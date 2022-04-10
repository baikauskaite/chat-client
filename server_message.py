class ServerMessage:
    """Server message is split to head and body. The body can then processed according to the heading."""

    # Splitting the message into a heading and a body
    def __init__(self, message):
        word_list = message.split()
        self.head = word_list.pop(0)
        self.body = word_list

    # Server's response to a correct first-handshake
    # TODO: newlines should be removed from the request's body
    def second_handshake(self):
        print("Hello, " + self.body)

    # Pairs of headings and functions to process the body for the matching heading
    headings = {
        "HELLO": second_handshake
    }

    # Match heading with a function to process the message's body
    # TODO: else case, when there's no matching heading in headings
    def match_heading(self):
        function = self.headings[self.head]
        if function is not None:
            function(self)
        else:
            pass