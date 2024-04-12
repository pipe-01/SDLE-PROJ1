import asyncio

from src.message import Message, Command
from src.zmq_client import ZMQClient
import os

def client(c1, msg):
    return c1.send_msg(msg)


def main():

        client(ZMQClient(), Message(Command.SUB, "topic1", "client1").toMultipart())

        client(ZMQClient(), Message(Command.PUT, "topic1", bytes("value1", "utf-8")).toMultipart())
        client(ZMQClient(), Message(Command.GET, "topic1", "client1").toMultipart())

        client(ZMQClient(), Message(Command.UNSUB, "topic1", "client1").toMultipart())
        client(ZMQClient(), Message(Command.PUT, "topic1", b"value2").toMultipart())

        client(ZMQClient(), Message(Command.SUB, "topic1", "client2").toMultipart())

        client(ZMQClient(), Message(Command.PUT, "topic1", b"value3").toMultipart())

        client(ZMQClient(), Message(Command.GET, "topic1", "client1").toMultipart())
        client(ZMQClient(), Message(Command.GET, "topic1", "client1").toMultipart())
        client(ZMQClient(), Message(Command.GET, "topic1", "client1").toMultipart())
        client(ZMQClient(), Message(Command.GET, "topic1", "client2").toMultipart())
        client(ZMQClient(), Message(Command.GET, "topic1", "client2").toMultipart())

        client(ZMQClient(), Message(Command.UNSUB, "topic1", "client1").toMultipart())
        client(ZMQClient(), Message(Command.PUT, "topic2", "value3").toMultipart())


if __name__ == '__main__':
    main()
