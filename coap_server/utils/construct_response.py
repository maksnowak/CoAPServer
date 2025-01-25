from coap_server.utils.constants import CoapCode, CoapMessage


def construct_response(
    request: CoapMessage, code: CoapCode, payload: bytes
) -> CoapMessage:
    """
    Function for convenient constructing response and to reduce duplicated code.
    """

    return CoapMessage(
        header_version=request.header_version,
        header_type=request.header_type,
        header_token_length=request.header_token_length,
        header_code=code,
        header_mid=request.header_mid,
        token=request.token,
        options={},
        payload=payload,
    )
