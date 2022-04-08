class ServerMessage:
    """Server message is split to head and body. The body can then processed according to the heading."""

    def __init__(self, message):
        word_list = message.split()
        self.head = word_list[0]
        self.body = word_list.pop(0)

    def second_handshake(self):
        pass

    headings = {
        "HELLO": second_handshake
    }

    def match_heading(self):
        value = self.headings[self.head]
        if value is None:
            pass
        else:
            value()
