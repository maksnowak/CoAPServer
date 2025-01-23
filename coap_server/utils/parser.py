from coap_server.utils.constants import CoapCode, CoapMessage, CoapOption


def parse_message(data: bytes) -> CoapMessage:
    """
    Parse the CoAP message data and return a CoapMessage.

    :param data: CoAP request data
    :type data: bytes

    :return: CoAP request data
    :rtype: CoapRequest
    """

    header_version = (0xC0 & data[0]) >> 6
    header_type = (0x30 & data[0]) >> 4
    header_token_length = (0x0F & data[0]) >> 0
    header_class = (data[1] >> 5) & 0x07
    header_code = (data[1] >> 0) & 0x1F
    header_code_decoded = f"{header_class}.{header_code:02}"
    header_mid = (data[2] << 8) | data[3]
    token = data[4 : 4 + header_token_length]
    payload_marker = data.find(
        b"\xff"
    )  # FIXME: 0xFF can be present in the option values
    if payload_marker != -1:
        options = data[
            4 + header_token_length : payload_marker
        ]  # TODO: extended options
    else:
        options = data[4 + header_token_length :]
    payload = data[payload_marker + 1 :]

    options_parsed: dict[CoapOption, bytes] = {}
    option_code = 0
    while options:
        option_delta = (options[0] & 0xF0) >> 4
        option_length = options[0] & 0x0F
        options = options[1:]
        option_value = options[:option_length]
        options = options[option_length:]
        option_code += option_delta
        options_parsed[CoapOption(option_code)] = option_value

    return CoapMessage(
        header_version=header_version,
        header_type=header_type,
        header_token_length=header_token_length,
        header_code=CoapCode(header_code_decoded),
        header_mid=header_mid,
        token=token,
        options=options_parsed,
        payload=payload,
    )


def encode_message(message: CoapMessage) -> bytes:
    data = bytes()

    # First byte: Version (2 bits), Type (2 bits), Token Length (4 bits)
    first_byte = (
        (message.header_version << 6)
        | (message.header_type << 4)
        | message.header_token_length
    )

    # Second byte: Class (3 bits), Code (5 bits)
    class_, code = message.header_code.value.split(".", 1)
    second_byte = (int(class_) << 5) | int(code)

    # Message ID (2 bytes)
    mid_high = (message.header_mid >> 8) & 0xFF
    mid_low = message.header_mid & 0xFF

    # Combine all parts of header
    data += bytes([first_byte, second_byte, mid_high, mid_low]) + message.token

    # Options
    for option, value in message.options.items():
        option_delta = option.value
        option_length = len(value)
        data += bytes([option_delta << 4 | option_length])
        data += value

    if message.payload:
        data += bytes([0xFF])
        data += message.payload

    return data
