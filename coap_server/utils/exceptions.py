"""Custom exceptions for handling CoAP requests errors."""


class MethodNotAllowedError(Exception):
    pass


class BadRequestError(Exception):
    pass


class NotFoundError(Exception):
    pass
