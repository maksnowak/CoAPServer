import socket
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import pytest

from coap_server.server import CoAPServer
from coap_server.utils.constants import CoapCode, CoapMessage, CoapOption
from coap_server.utils.parser import encode_message, parse_message


def client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        server_address = ("127.0.0.1", 5683)

        request = CoapMessage(
            header_version=1,
            header_type=0,
            header_token_length=4,
            header_code=CoapCode.GET,
            header_mid=1337,
            token=b"1234",
            options={
                CoapOption.URI_PATH: b"/sensors/1/temperature",
            },
            payload=b"",
        )

        sock.sendto(encode_message(request), server_address)

        data = sock.recv(1024)
        response = parse_message(data)
        return response


def test_get(routes):
    server = CoAPServer(routes)
    server_thread = Thread(target=server.start, daemon=True)
    server_thread.start()

    try:
        response = client()

        assert response.header_version == 1
        assert response.header_type == 0
        assert response.header_token_length == 4
        assert response.header_code == CoapCode.CONTENT
        assert response.header_mid == 1337
        assert response.token == b"1234"
        assert response.options == {}
        assert response.payload == b"21"
    finally:
        server.shutdown()
        server_thread.join()


@pytest.mark.parametrize("num_clients", [1, 2, 3, 5, 10])
def test_multiple_requests(routes, num_clients):
    server = CoAPServer(routes)
    server_thread = Thread(target=server.start, daemon=True)
    server_thread.start()

    try:
        with ThreadPoolExecutor(max_workers=num_clients) as executor:
            responses = list(
                executor.map(lambda _: client(), range(num_clients))
            )

        for response in responses:
            assert response.payload == b"21"
    finally:
        server.shutdown()
        server_thread.join()
