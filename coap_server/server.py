import socket
from typing import MutableMapping

from coap_server.logger import logger
from coap_server.request_handler import RequestHandler
from coap_server.resources.base_resource import BaseResource


class CoAPServer:
    def __init__(
        self,
        routes: MutableMapping[str, BaseResource],
        host="127.0.0.1",
        port=5683,
    ):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.routes = routes
        self.handler = RequestHandler(self.routes)

    def start(self):
        self.running = True
        self.sock.bind((self.host, self.port))
        logger.info(f"CoAP Server started on {self.host}:{self.port}")

        while self.running:
            try:
                self.sock.settimeout(1)
                data, addr = self.sock.recvfrom(1024)
                logger.debug(f"Received data from {addr}")

                response = self.handler.handle_request(data)
                self.sock.sendto(response, addr)
                logger.debug(f"Sent response to {addr}")

            except socket.timeout:
                continue
            except OSError as e:
                logger.error(f"Server error: {e}")
                break

    def shutdown(self):
        self.running = False
        self.sock.close()
        logger.info("CoAP Server stopped")
