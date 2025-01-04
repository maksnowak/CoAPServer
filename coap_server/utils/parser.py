from coap_server.utils.constants import CoapRequest


def parse_request(data: bytes) -> CoapRequest:
    """
    Parse the CoAP request data and return a dictionary.

    :param data: CoAP request data
    :type data: bytes

    :return: CoAP request data as a dictionary
    :rtype: CoapRequest
    """
    raise NotImplementedError("parse_request function not implemented.")
