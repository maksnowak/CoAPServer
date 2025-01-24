import json

from coap_server.request_handler import RequestHandler
from coap_server.utils.constants import CoapCode, CoapMessage, CoapOption
from coap_server.utils.parser import encode_message, parse_message

obj_encoded = json.dumps({"name": "New device", "temperature": 30}).encode(
    "ascii"
)


def test_success(routes):
    handler = RequestHandler(routes)

    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.POST,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/devices",
        },
        payload=obj_encoded,
    )

    request_encoded = encode_message(request)
    response_encoded = handler.handle_request(request_encoded)
    response = parse_message(response_encoded)

    assert response.header_version == 1
    assert response.header_type == 0
    assert response.header_token_length == 4
    assert response.header_code == CoapCode.CREATED
    assert response.header_mid == 1337
    assert response.token == b"1234"
    assert response.options == {}
    assert response.payload == obj_encoded

    # Assert it was actually added
    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.GET,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/devices/3",
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
    assert response.payload == obj_encoded


def test_invalid_uri_id(routes):
    handler = RequestHandler(routes)

    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.POST,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/devices/1",
        },
        payload=obj_encoded,
    )

    request_encoded = encode_message(request)
    response_encoded = handler.handle_request(request_encoded)
    response = parse_message(response_encoded)

    assert response.header_version == 1
    assert response.header_type == 0
    assert response.header_token_length == 4
    assert response.header_code == CoapCode.METHOD_NOT_ALLOWED
    assert response.header_mid == 1337
    assert response.token == b"1234"
    assert response.options == {}
    assert (
        response.payload
        == b'{"error": "Method not allowed for this resource"}'
    )


def test_invalid_uri_temperature(routes):
    handler = RequestHandler(routes)

    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.POST,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/devices/1/temperature",
        },
        payload=obj_encoded,
    )

    request_encoded = encode_message(request)
    response_encoded = handler.handle_request(request_encoded)
    response = parse_message(response_encoded)

    assert response.header_version == 1
    assert response.header_type == 0
    assert response.header_token_length == 4
    assert response.header_code == CoapCode.METHOD_NOT_ALLOWED
    assert response.header_mid == 1337
    assert response.token == b"1234"
    assert response.options == {}
    assert (
        response.payload
        == b'{"error": "Method not allowed for this resource"}'
    )


def test_invalid_json(routes):
    handler = RequestHandler(routes)

    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.POST,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/devices",
        },
        payload=b'{"name": "New name"',
    )

    request_encoded = encode_message(request)
    response_encoded = handler.handle_request(request_encoded)
    response = parse_message(response_encoded)

    assert response.header_version == 1
    assert response.header_type == 0
    assert response.header_token_length == 4
    assert response.header_code == CoapCode.BAD_REQUEST
    assert response.header_mid == 1337
    assert response.token == b"1234"
    assert response.options == {}
    assert response.payload == b'{"error": "Invalid payload"}'


def test_missing_fields(routes):
    handler = RequestHandler(routes)

    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.POST,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/devices",
        },
        payload=b'{"name": "New name"}',
    )

    request_encoded = encode_message(request)
    response_encoded = handler.handle_request(request_encoded)
    response = parse_message(response_encoded)

    assert response.header_version == 1
    assert response.header_type == 0
    assert response.header_token_length == 4
    assert response.header_code == CoapCode.BAD_REQUEST
    assert response.header_mid == 1337
    assert response.token == b"1234"
    assert response.options == {}
    assert response.payload == b'{"error": "Invalid payload"}'
