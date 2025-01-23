from coap_server.resources.base_resource import BaseResource
from coap_server.utils.constants import CoapCode, CoapMessage
import json


class DevicesResource(BaseResource):
    def __init__(self):
        self.devices = {1: "Device 1", 2: "Device 2"}

    def get(self, request: CoapMessage) -> CoapMessage:
        response = CoapMessage(
            header_version=request.header_version,
            header_type=request.header_type,
            header_token_length=request.header_token_length,
            header_code=CoapCode.CONTENT,
            header_mid=request.header_mid,
            token=request.token,
            options={},
            payload=str(self.devices).encode("ascii"),
        )

        return response

    def post(self, request: CoapMessage) -> CoapMessage:
        try:
            device = json.loads(request.payload.decode())
            self.devices[device["id"]] = device["name"]

            response = CoapMessage(
                header_version=request.header_version,
                header_type=request.header_type,
                header_token_length=request.header_token_length,
                header_code=CoapCode.CREATED,
                header_mid=request.header_mid,
                token=request.token,
                options={},
                payload=f"Device {device['id']} created".encode("ascii"),
            )

        except Exception:
            response = CoapMessage(
                header_version=request.header_version,
                header_type=request.header_type,
                header_token_length=request.header_token_length,
                header_code=CoapCode.BAD_REQUEST,
                header_mid=request.header_mid,
                token=request.token,
                options={},
                payload=b"",
            )

        return response
