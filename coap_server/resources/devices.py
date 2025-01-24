from coap_server.resources.base_resource import BaseResource
from coap_server.utils.constants import CoapCode, CoapMessage
import json


class DevicesResource(BaseResource):
    def __init__(self, objects: dict[int, dict[str, str]]):
        # objects = {
        #     device_id: {
        #         "name": "Device 1",
        #     },
        #     ...
        # }
        self.objects = objects

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
                payload=json.dumps(self.objects).encode("ascii"),
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
                payload=json.dumps(self.objects[device_id]).encode("ascii"),
            )

        return response

    def post(self, request: CoapMessage) -> CoapMessage:
        try:
            uri = request.uri
            if uri != "/devices":
                raise ValueError

            device = json.loads(request.payload.decode())

            ids = self.objects.keys()
            new_id = max(ids) + 1 if ids else 1
            self.objects[new_id] = device

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

            if device_id not in self.objects:
                raise ValueError

            device = json.loads(request.payload.decode())
            # TODO: verify received device data is valid

            self.objects[int(device_id)] = device

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

    def delete(self, request: CoapMessage) -> CoapMessage:
        try:
            uri = request.uri
            device_id = int(uri.rsplit("/", 1)[-1])

            if device_id not in self.objects:
                raise ValueError

            self.objects.pop(device_id)

            response = CoapMessage(
                header_version=request.header_version,
                header_type=request.header_type,
                header_token_length=request.header_token_length,
                header_code=CoapCode.DELETED,
                header_mid=request.header_mid,
                token=request.token,
                options={},
                payload=b"Device deleted",
            )

        except ValueError:
            response = CoapMessage(
                header_version=request.header_version,
                header_type=request.header_type,
                header_token_length=request.header_token_length,
                header_code=CoapCode.NOT_FOUND,
                header_mid=request.header_mid,
                token=request.token,
                options={},
                payload=b'{"error": "Device not found"}',
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
