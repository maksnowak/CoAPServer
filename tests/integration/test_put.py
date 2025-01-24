import json

from coap_server.request_handler import RequestHandler
from coap_server.utils.constants import CoapCode, CoapMessage, CoapOption
from coap_server.utils.parser import encode_message, parse_message

obj_encoded = json.dumps({"name": "New name", "temperature": 30}).encode(
    "ascii"
)


def test_success(routes):
    handler = RequestHandler(routes)

    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.PUT,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/sensors/1",
        },
        payload=obj_encoded,
    )

    request_encoded = encode_message(request)
    response_encoded = handler.handle_request(request_encoded)
    response = parse_message(response_encoded)

    assert response.header_version == 1
    assert response.header_type == 0
    assert response.header_token_length == 4
    assert response.header_code == CoapCode.CHANGED
    assert response.header_mid == 1337
    assert response.token == b"1234"
    assert response.options == {}
    assert response.payload == obj_encoded

    # Check it was actually modified
    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.GET,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/sensors/1",
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


def test_invalid_id_not_exists(routes):
    handler = RequestHandler(routes)

    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.PUT,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/sensors/123",
        },
        payload=obj_encoded,
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
    assert response.payload == b'{"error": "Not found: /sensors/123"}'


def test_invalid_id_not_int(routes):
    handler = RequestHandler(routes)

    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.PUT,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/sensors/abc",
        },
        payload=b'{"name": "New name"}',
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
    assert response.payload == b'{"error": "Not found: /sensors/abc"}'


def test_invalid_json(routes):
    handler = RequestHandler(routes)

    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.PUT,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/sensors/1",
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
        header_code=CoapCode.PUT,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/sensors/1",
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


def test_update_temperature(routes):
    handler = RequestHandler(routes)

    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.PUT,
        header_mid=1337,
        token=b"1234",
        options={
            CoapOption.URI_PATH: b"/sensors/1/temperature",
        },
        payload=b"40",
    )

    request_encoded = encode_message(request)
    response_encoded = handler.handle_request(request_encoded)
    response = parse_message(response_encoded)

    assert response.header_version == 1
    assert response.header_type == 0
    assert response.header_token_length == 4
    assert response.header_code == CoapCode.CHANGED
    assert response.header_mid == 1337
    assert response.token == b"1234"
    assert response.options == {}
    assert response.payload == b'{"name": "sensor 1", "temperature": 40}'

    # Check it was actually modified
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
    assert response.payload == b"40"
