import socket

from coap_server.utils.constants import CoapCode, CoapMessage, CoapOption
from coap_server.utils.parser import parse_message, encode_message


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
            CoapOption.URI_PATH: b"/temperature",
        },
        payload=b"",
    )

    sock.sendto(encode_message(request), server_address)

    data = sock.recv(1024)
    print(data)
    response = parse_message(data)
    print(response)
