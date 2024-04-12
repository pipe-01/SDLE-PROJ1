import unittest
from src.client import client
from src.message import Message, Command


class ClientTest(unittest.TestCase):
    def test_something(self):
        msg = Message(Command.SUB, "topic1", "client1").toMultipart()
        client = client(ZMQClient(), msg)
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
