from coap_server.utils.constants import CoapRequest, CoapOption


def parse_request(data: bytes) -> CoapRequest:
    """
    Parse the CoAP request data and return a dictionary.

    :param data: CoAP request data
    :type data: bytes

    :return: CoAP request data as a dictionary
    :rtype: CoapRequest
    """
    header_version = (0xC0 & data[0]) >> 6
    header_type    = (0x30 & data[0]) >> 4
    header_tkl     = (0x0F & data[0]) >> 0
    header_class   = (data[1] >> 5) & 0x07
    header_code    = (data[1] >> 0) & 0x1F
    header_mid     = (data[2] << 8) | data[3]
    token          = data[4:4 + header_tkl]
    payload_marker = data.find(b"\xFF") # FIXME: 0xFF can be present in the option values
    options        = data[4 + header_tkl:payload_marker]
    payload        = data[payload_marker + 1:]

    options: dict[CoapOption, bytes] = {}
    option_code = 0
    while options:
        option_delta = (options[0] & 0xF0) >> 4
        option_length = (options[0] & 0x0F)
        options = options[1:]
        option_value = options[:option_length]
        options = options[option_length:]
        option_code += option_delta
        options[CoapOption(option_code)] = option_value
    
    return CoapRequest(
        method=header_code,
        options=options,
        uri=compose_uri(options),
        payload=payload
    )
    
def compose_uri(options: dict[CoapOption, bytes]) -> str:
    """
    Compose the URI from the options.

    :param options: CoAP options
    :type options: dict[CoapOption, bytes]

    :return: URI
    :rtype: str
    """
    uri = ""
    if CoapOption.URI_PATH in options:
        uri += "/" + "/".join(options[CoapOption.URI_PATH].decode().split(","))
    if CoapOption.URI_QUERY in options:
        uri += "?" + "&".join(options[CoapOption.URI_QUERY].decode().split(","))
    return uri