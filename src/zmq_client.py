import zmq

REQUEST_TIMEOUT = 2500
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://localhost:5555"


class ZMQClient:

    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(SERVER_ENDPOINT)

    def send_msg(self, msg):
        self.socket.send_multipart(msg)
        print("Sending ", msg)
        retries_left = REQUEST_RETRIES
        while True:
            if (self.socket.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
                resp = self.socket.recv()
                print("Received: \"%s\"" % resp)
                return resp
            retries_left -= 1
            print("No response from server")
            # Socket is confused. Close and remove it.
            self.socket.setsockopt(zmq.LINGER, 0)
            self.socket.close()
            if retries_left == 0:
                return "Server seems to be offline, abandoning"

            print("Reconnecting to server…")
            # Create new connection
            self.socket = self.context.socket(zmq.REQ)
            self.socket.connect(SERVER_ENDPOINT)
            print("Resending ", msg)
            self.socket.send_multipart(msg)

    def close(self):
        self.socket.close()
        self.context.term()
