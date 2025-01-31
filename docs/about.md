# CoAP Protocol Overview

The CoAP protocol is a binary protocol based on UDP, designed for use on resource-constrained devices, particularly for IoT applications. It is modeled after HTTP and uses a similar resource structure as the REST model. Requests are identified with `0.*` codes, followed by a response containing one of three types of codes.

## Message Processing

Message structure:
- Header, 4 bytes:
  - Version
  - Message type:
    - Request, confirmable or non-confirmable
    - Response, with data or data sent later
  - Token length
  - Message code
  - Message ID
- Token, 0 to 8 bytes
- Options (optional)
- Payload (optional)
  - Begins after the `0xFF` marker

After processing a request, a response or error is returned. Successful responses are marked with `2.*`, client-side errors with `4.*`, and server-side errors with `5.*`.

# Key Structures and Functions

## `server.py`

This file contains the definition of the main server class, `CoAPServer`. The class takes as input parameters a `routes` structure containing available resources, a `host` with the server's IP address, and a `port` specifying the port the server listens on.

The class has two methods – `start()` and `shutdown()`. The first starts the server, while the second stops it.

## `request_handler.py`

This file defines the `RequestHandler` class. The constructor receives a `routes` structure, similar to `CoAPServer`. The class includes a `handle_request()` method, which takes a byte sequence representing a CoAP request and returns the server's response as a byte sequence.

Request processing uses the `parse_message()` and `encode_message()` functions described below.

## `utils/parser.py`

### `parse_message()`

This function takes a byte sequence representing a CoAP request as input and returns a `CoapMessage` structure containing request details.

### `encode_message()`

This function takes a `CoapMessage` structure containing the server's response information and returns a byte sequence representing the response.

## `utils/construct_response.py`

This file contains the `construct_response()` function, used by specific resources. It takes a request in the form of a `CoapMessage` structure, a response code, and response content. The function returns a `CoapMessage` structure representing the server's response.

# Configuration Flags

The CoAP server implementation includes configuration flags provided as command-line arguments:
- `--host` – Server IP address
- `--port` – Port number the server listens on
- `--verbose` – Log verbosity level:
    - `-v` – Warnings only
    - `-vv` – Warnings and informational logs
    - `-vvv` – Warnings, informational logs, and debug logs

# Log Format

Logs follow this format:

```bash
<timestamp> [<log_level>] <message>
```

Where:
- `timestamp` – Date and time of the event
- `log_level` – Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `message` – Log content

Example logs:

```bash
2025-01-24 08:50:01,812 [DEBUG] Received data from ('127.0.0.1', 48990)
2025-01-24 08:50:01,812 [DEBUG] Handling request: CoapMessage(header_version=1, header_type=0, header_token_length=4, header_code=<CoapCode.GET: '0.01'>, header_mid=1337, token=b'1234', options={<CoapOption.URI_PATH: 11>: b'/sensors'}, payload=b'')
2025-01-24 08:50:01,815 [INFO] Received GET request for URI: /sensors
2025-01-24 08:50:01,815 [DEBUG] Returning all sensor data
2025-01-24 08:50:01,815 [INFO] Request to /sensors handled successfully
2025-01-24 08:50:01,815 [DEBUG] Sent response to ('127.0.0.1', 48990)
```

# Tools Used

- `Docker` – Application containerization
- `poetry` – Dependency management
- `ruff` – Linter and formatter
- `mypy` – Static analysis
- `pytest` – Unit and integration testing
- `typer` – CLI interface creation

## CLI Tool

To simplify sending requests to a CoAP server, a CLI tool is available, similar to `curl`. This tool allows sending `GET`, `POST`, `PUT`, and `DELETE` requests to a CoAP server.

### Usage

To run the CLI tool, execute:

```bash
python cli.py <uri> [options]
```

Where:
- `uri` – CoAP server URL
- `options` – Additional options depending on the request:
    - `--method` – Request method (`GET`, `POST`, `PUT`, `DELETE`)
    - `--data` – Data to send with the request (for `POST` and `PUT`)
    - `--verbose` – Log verbosity level:
        - `-v` – Warnings only
        - `-vv` – Warnings and informational logs
        - `-vvv` – Warnings, informational logs, and debug logs

# Testing

## Unit Tests

Unit tests cover only functions parsing CoAP messages. These tests verify the correctness of `parse_message()` and `encode_message()` functions.

## Integration Tests

Integration tests validate client-server communication by simulating requests to the server and checking whether responses are correct and resources are updated properly.

Additionally, integration tests assess system stability by ensuring the server handles multiple clients concurrently.

## Manual Testing

Manual tests involve sending requests to the CoAP server using the CLI tool and verifying correct server responses.

Example manual test:

### 1. Start the server:

```bash
make run
```

### 2. Send a GET request to `/sensors`:

```bash
poetry run python cli.py coap://localhost:5683/sensors
```

or

```bash
source .venv/bin/activate
python cli.py coap://localhost:5683/sensors
```

### 3. Expected output:

Client:

```
Response Code: 2.05 Content
Data: {"1": {"name": "Sensor 1", "temperature": 21}, "2": {"name": "Sensor 2", "temperature": 25}}
```

Server:

```
2025-01-24 09:48:57,999 [INFO] Received GET request for URI: /sensors
2025-01-24 09:48:57,999 [DEBUG] Returning all sensor data
2025-01-24 09:48:57,999 [INFO] Request to /sensors handled successfully
```

The request was handled correctly, and the server returned response code `2.05 Content` along with the available sensor data.

To verify CLI correctness, the same test was run using an external client library `aiocoap`. The responses matched, confirming correct CoAP protocol implementation.

## Coverage

The server's test coverage is 82%. The `htmlcov/index.html` file (generated by `make test`) provides a visual breakdown of covered lines and areas lacking test coverage.

