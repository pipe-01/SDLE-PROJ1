import zmq
import zmq.asyncio


class ZMQServer:

    def __init__(self):
        self.context = zmq.asyncio.Context()
        self.socket = self.context.socket(zmq.REP)
        server_url = "tcp://*:5555"
        self.socket.bind(server_url)

    async def receive(self, callback):
        while True:
            msg = await self.socket.recv_multipart()
            self.socket.send(callback(msg))
