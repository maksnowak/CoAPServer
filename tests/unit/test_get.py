import json

from coap_server.request_handler import RequestHandler
from coap_server.utils.constants import CoapCode, CoapMessage, CoapOption
from coap_server.utils.parser import parse_message, encode_message


def test_success(routes):
    handler = RequestHandler(routes)

    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.GET,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/temperature/1",
        },
        payload=b"",
    )

    request_encoded = encode_message(request)
    response_encoded = handler.handle_request(request_encoded)
    response = parse_message(response_encoded)

    assert response.header_version == 1
    assert response.header_type == 0
    assert response.header_token_length == 4
    assert response.header_code == CoapCode.CONTENT
    assert response.header_mid == 1337
    assert response.token == b"1234"
    assert response.options == {}
    assert response.payload == b"Temperature is 22C"


def test_not_found(routes):
    handler = RequestHandler(routes)

    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.GET,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/temperature/2",
        },
        payload=b"",
    )

    request_encoded = encode_message(request)
    response_encoded = handler.handle_request(request_encoded)
    response = parse_message(response_encoded)

    assert response.header_version == 1
    assert response.header_type == 0
    assert response.header_token_length == 4
    assert response.header_code == CoapCode.NOT_FOUND
    assert response.header_mid == 1337
    assert response.token == b"1234"
    assert response.options == {}
    assert response.payload == b"Sensor not found"


def test_devices_list(devices, routes):
    handler = RequestHandler(routes)

    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.GET,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/devices",
        },
        payload=b"",
    )

    request_encoded = encode_message(request)
    response_encoded = handler.handle_request(request_encoded)
    response = parse_message(response_encoded)

    assert response.header_version == 1
    assert response.header_type == 0
    assert response.header_token_length == 4
    assert response.header_code == CoapCode.CONTENT
    assert response.header_mid == 1337
    assert response.token == b"1234"
    assert response.options == {}
    assert response.payload == json.dumps(devices).encode("ascii")


def test_devices_retrieve(routes):
    handler = RequestHandler(routes)

    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.GET,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/devices/1",
        },
        payload=b"",
    )

    request_encoded = encode_message(request)
    response_encoded = handler.handle_request(request_encoded)
    response = parse_message(response_encoded)

    assert response.header_version == 1
    assert response.header_type == 0
    assert response.header_token_length == 4
    assert response.header_code == CoapCode.CONTENT
    assert response.header_mid == 1337
    assert response.token == b"1234"
    assert response.options == {}
    assert response.payload == b'{"name": "Device 1"}'
