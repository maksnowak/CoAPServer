from coap_server.resources.base_resource import BaseResource
from coap_server.utils.constants import CoapCode, CoapMessage
import json


class DevicesResource(BaseResource):
    def __init__(self):
        self.devices = {
            1: {
                "name": "Device 1",
            },
            2: {
                "name": "Device 2",
            },
        }

    def get(self, request: CoapMessage) -> CoapMessage:
        uri = request.uri

        if uri == "/devices/":
            response = CoapMessage(
                header_version=request.header_version,
                header_type=request.header_type,
                header_token_length=request.header_token_length,
                header_code=CoapCode.CONTENT,
                header_mid=request.header_mid,
                token=request.token,
                options={},
                payload=json.dumps(self.devices).encode("ascii"),
            )
        else:
            device_id = int(uri.rsplit("/", 1)[-1])

            response = CoapMessage(
                header_version=request.header_version,
                header_type=request.header_type,
                header_token_length=request.header_token_length,
                header_code=CoapCode.CONTENT,
                header_mid=request.header_mid,
                token=request.token,
                options={},
                payload=json.dumps(self.devices[device_id]).encode("ascii"),
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

    def put(self, request: CoapMessage) -> CoapMessage:
        try:
            uri = request.uri
            device_id = int(uri.rsplit("/", 1)[-1])

            if device_id not in self.devices:
                raise ValueError

            device = json.loads(request.payload.decode())
            # TODO: verify received device data is valid

            self.devices[int(device_id)] = device

            response = CoapMessage(
                header_version=request.header_version,
                header_type=request.header_type,
                header_token_length=request.header_token_length,
                header_code=CoapCode.CHANGED,
                header_mid=request.header_mid,
                token=request.token,
                options={},
                payload=json.dumps(device).encode("ascii"),
            )

        except ValueError:  # id doesn't exist or not int
            response = CoapMessage(
                header_version=request.header_version,
                header_type=request.header_type,
                header_token_length=request.header_token_length,
                header_code=CoapCode.BAD_REQUEST,
                header_mid=request.header_mid,
                token=request.token,
                options={},
                payload=b'{"error": "Invalid resource id"}',
            )

        except Exception as e:
            response = CoapMessage(
                header_version=request.header_version,
                header_type=request.header_type,
                header_token_length=request.header_token_length,
                header_code=CoapCode.BAD_REQUEST,
                header_mid=request.header_mid,
                token=request.token,
                options={},
                payload=json.dumps({"error": str(e)}).encode("ascii"),
            )

        return response
