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
    options = data[4 + header_token_length :]
    options_parsed: dict[CoapOption, bytes] = {}
    option_code = 0
    payload = b""
    while options and options[0] != 0xFF:
        delta, length = (options[0] & 0xF0) >> 4, options[0] & 0x0F
        options = options[1:]

        # Handle extended option delta
        if delta == 13:
            delta = options[0] + 13
            options = options[1:]
        elif delta == 14:
            delta = (options[0] << 8) + options[1] + 269
            options = options[2:]
        elif delta == 15:
            raise ValueError(
                "Invalid option delta: 15 is reserved for payload marker"
            )

        # Handle extended option length
        if length == 13:
            length = options[0] + 13
            options = options[1:]
        elif length == 14:
            length = (options[0] << 8) + options[1] + 269
            options = options[2:]
        elif length == 15:
            raise ValueError("Invalid option length: 15 is reserved")

        option_code += delta
        options_parsed[CoapOption(option_code)] = options[:length]
        options = options[length:]

    if options:
        if options[0] == 0xFF:
            payload = options[1:]
        else:
            raise ValueError("Invalid message: missing payload marker")

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
    prev_option = 0
    for option, value in sorted(message.options.items()):
        option_delta = option.value - prev_option
        option_length = len(value)

        # Handle extended option delta
        if option_delta >= 269:
            data += bytes(
                [14 << 4 | (option_length if option_length < 13 else 13)]
            )
            delta_ext = option_delta - 269
            data += bytes([delta_ext >> 8, delta_ext & 0xFF])
        elif option_delta >= 13:
            data += bytes(
                [13 << 4 | (option_length if option_length < 13 else 13)]
            )
            data += bytes([option_delta - 13])
        else:
            data += bytes(
                [
                    option_delta << 4
                    | (option_length if option_length < 13 else 13)
                ]
            )

        # Handle extended option length
        if option_length >= 269:
            if option_delta < 13:
                data = data[:-1] + bytes([option_delta << 4 | 14])
            length_ext = option_length - 269
            data += bytes([length_ext >> 8, length_ext & 0xFF])
        elif option_length >= 13:
            if option_delta < 13:
                data = data[:-1] + bytes([option_delta << 4 | 13])
            data += bytes([option_length - 13])

        data += value
        prev_option = option.value

    if message.payload:
        data += bytes([0xFF])
        data += message.payload

    return data
