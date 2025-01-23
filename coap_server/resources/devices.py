from coap_server.resources.base_resource import BaseResource
from coap_server.utils.constants import CoapCode, CoapMessage
import json


class DevicesResource(BaseResource):
    def __init__(self, devices: dict[int, dict[str, str]]):
        # devices = {
        #     device_id: {
        #         "name": "Device 1",
        #     },
        #     ...
        # }
        self.devices = devices

    def get(self, request: CoapMessage) -> CoapMessage:
        uri = request.uri

        if uri == "/devices":
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
            uri = request.uri
            if uri != "/devices":
                raise ValueError

            device = json.loads(request.payload.decode())

            ids = self.devices.keys()
            new_id = max(ids) + 1 if ids else 1
            self.devices[new_id] = device

            response = CoapMessage(
                header_version=request.header_version,
                header_type=request.header_type,
                header_token_length=request.header_token_length,
                header_code=CoapCode.CREATED,
                header_mid=request.header_mid,
                token=request.token,
                options={},
                payload=b"Device created",
            )

        except json.JSONDecodeError:
            response = CoapMessage(
                header_version=request.header_version,
                header_type=request.header_type,
                header_token_length=request.header_token_length,
                header_code=CoapCode.BAD_REQUEST,
                header_mid=request.header_mid,
                token=request.token,
                options={},
                payload=b'{"error": "Invalid device data"}',
            )

        except ValueError:
            response = CoapMessage(
                header_version=request.header_version,
                header_type=request.header_type,
                header_token_length=request.header_token_length,
                header_code=CoapCode.METHOD_NOT_ALLOWED,
                header_mid=request.header_mid,
                token=request.token,
                options={},
                payload=b'{"error": "POST method is not allowed for a specific device"}',
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

    def __repr__(self) -> str:
        return f"DevicesResource(devices={self.devices})"
