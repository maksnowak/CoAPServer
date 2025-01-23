from coap_server.request_handler import RequestHandler
from coap_server.utils.constants import CoapCode, CoapMessage, CoapOption
from coap_server.utils.parser import parse_message, encode_message


def test_success():
    handler = RequestHandler()

    request = CoapMessage(
        header_version=1,
        header_type=0,
        header_token_length=4,
        header_code=CoapCode.PUT,
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
    assert response.header_code == CoapCode.CHANGED
    assert response.header_mid == 1337
    assert response.token == b"1234"
    assert response.options == {}
    assert response.payload == b'{"name": "New name"}'
