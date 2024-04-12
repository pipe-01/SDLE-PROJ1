import zmq
import sys
from typing import List
from src.message import Message, Command


class ZMQClient:

    def __init__(self, argv):
        identity = argv[0]
        print(f'Start client with id {identity}')
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://127.0.0.1:5555")
        self.connect(identity)

    def connect(self, identity):
        try:
            while True:
                com = input("Write a message\nSUB <TOPIC>\nUNSUB <TOPIC>\nGET <TOPIC>\nPUT <TOPIC> <MESSAGE>\n: ")
                com = com.split(' ')
                op = com[0].lower()

                if (op == 'sub'):
                    message = Message(Command.SUB, com[1], identity).toMultipart()
                    send_msg(self.socket, message)
                elif (op == 'unsub'):
                    message = Message(Command.UNSUB, com[1], identity).toMultipart()
                    send_msg(self.socket, message)
                elif (op == 'put'):
                    message = Message(Command.PUT, com[1], bytes(com[2], "utf-8")).toMultipart()
                    send_msg(self.socket, message)
                elif (op == 'get'):
                    message = Message(Command.GET, com[1], identity).toMultipart()
                    send_msg(self.socket, message)
                else:
                    print(f'Not a valid option, please enter a valid one')
        except KeyboardInterrupt:
            print("Closing connection...")
            self.socket.close()
            self.context.term()

    def send_msg(self, msg):
        self.socket.send_multipart(msg)
        print("Sending ", msg)
        resp = self.socket.recv()
        print("Received: \"%s\"" % resp)
        return resp


def send_msg(socket, msg):
    socket.send_multipart(msg)
    print("Sending ", msg)
    resp = socket.recv()
    print("Received: \"%s\"" % resp)
    return resp


def main(argv: int):
    # client id
    # print(f'Start client with id {identity}')

    #  context = zmq.Context()
    # socket = context.socket(zmq.REQ)
    # socket.connect("tcp://127.0.0.1:5555")
    ZMQClient(argv)


if __name__ == '__main__':
    main(sys.argv[1:])
