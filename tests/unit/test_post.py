from coap_server.request_handler import RequestHandler
from coap_server.utils.constants import CoapCode, CoapMessage, CoapOption
from coap_server.utils.parser import parse_message, encode_message


def test_success():
    handler = RequestHandler()

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
    assert response.header_code == CoapCode.CREATED
    assert response.header_mid == 1337
    assert response.token == b"1234"
    assert response.options == {}
    assert response.payload == b"Device created"

    # Check it was actually added
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
    assert (
        response.payload
        == b'{"1": {"name": "Device 1"}, "2": {"name": "Device 2"}, "3": {"name": "New name"}}'
    )


def test_failure_incorrect_uri():
    handler = RequestHandler()

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
        payload=b'{"name": "New name"}',
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
        == b'{"error": "POST method is not allowed for a specific device"}'
    )

    # Check it was actually not added
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
    assert response.payload == b'{"1": {"name": "Device 1"}, "2": {"name": "Device 2"}}'


def test_failure_invalid_json():
    handler = RequestHandler()

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
    assert response.payload == b'{"error": "Invalid device data"}'

    # Check it was actually not added
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
    assert response.payload == b'{"1": {"name": "Device 1"}, "2": {"name": "Device 2"}}'
