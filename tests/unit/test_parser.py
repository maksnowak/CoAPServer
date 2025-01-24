from coap_server.utils.constants import CoapCode, CoapMessage, CoapOption
from coap_server.utils.parser import parse_message, encode_message


def test_encode_message():
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
    assert request_encoded == b"D\x01\x0591234\xbe/temperature/1"


def test_parse_message():
    response_encoded = b"D\x01\x0591234\xbe/temperature/1"

    response = parse_message(response_encoded)

    assert response.header_version == 1
    assert response.header_type == 0
    assert response.header_token_length == 4
    assert response.header_code == CoapCode.GET
    assert response.header_mid == 1337
    assert response.token == b"1234"
    assert response.options == {
        CoapOption.URI_PATH: b"/temperature/1",
    }
    assert response.payload == b""
