import socket
from coap_server.request_handler import RequestHandler


class CoAPServer:
    def __init__(self, host="127.0.0.1", port=5683):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.handler = RequestHandler()

    def start(self):
        self.sock.bind((self.host, self.port))
        print(f"\nCoAP Server started on {self.host}:{self.port}")
        while True:
            data, addr = self.sock.recvfrom(1024)
            response = self.handler.handle_request(data)
            self.sock.sendto(response, addr)
