from enum import Enum


class Command(Enum):
    SUB = b"sub"
    UNSUB = b"unsub"
    PUT = b"put"
    GET = b"get"


class Message:

    def __init__(self, cmd: Command, topicName, value=None):
        self.cmd = cmd
        self.topicName = topicName
        self.value = value

    def toMultipart(self):
        return [self.cmd.value, bytes(self.topicName, "utf-8"),
                (self.value if isinstance(self.value, bytes) else bytes(self.value, "utf-8"))]

    def listToMessage(msgList):
        if (len(msgList) == 3):
            return Message(Command(msgList[0]), msgList[1].decode("utf-8"), msgList[2])
        else:
            raise Exception("list must be size 3")
