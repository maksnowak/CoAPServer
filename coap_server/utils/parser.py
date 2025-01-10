from coap_server.utils.constants import CoapRequest


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
    options        = data[12:16]
    if data[16] == 0xFF: # payload marker
        payload = data[17:]
    else:
        payload = None
    