#!/usr/bin/env python3

import logging
import socket
from urllib.parse import urlparse

import typer

from coap_server.utils.constants import CoapCode, CoapMessage, CoapOption
from coap_server.utils.parser import encode_message, parse_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("coap_client")

app = typer.Typer()


@app.command()
def request(
    method: str = typer.Option(
        "GET", help="HTTP method (GET/POST/PUT/DELETE)"
    ),
    uri: str = typer.Argument(..., help="CoAP URI (coap://host:port/path)"),
    data: str = typer.Option(None, help="Data to send in request body"),
    verbose: int = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        help="Increase verbosity level (-v = warning, -vv = info, -vvv = debug)",
    ),
):
    """Send CoAP request to server"""

    # Adjust logging level based on verbosity
    log_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    log_level = log_levels[min(verbose, len(log_levels) - 1)]
    logger.setLevel(log_level)

    # Parse URI
    parsed_uri = urlparse(uri)
    if parsed_uri.scheme != "coap":
        logger.error("Invalid URI: URI must use coap:// scheme")
        raise typer.BadParameter("URI must use coap:// scheme")

    host = parsed_uri.hostname
    port = parsed_uri.port or 5683
    path = parsed_uri.path

    logger.info(f"Sending {method.upper()} request to {host}:{port}{path}")

    # Map method string to CoapCode enum
    method_map = {
        "GET": CoapCode.GET,
        "POST": CoapCode.POST,
        "PUT": CoapCode.PUT,
        "DELETE": CoapCode.DELETE,
    }

    if method.upper() not in method_map:
        logger.error(f"Unsupported method: {method.upper()}")
        raise typer.BadParameter(
            "Method must be one of GET, POST, PUT, DELETE"
        )

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            coap_request = CoapMessage(
                header_version=1,
                header_type=0,
                header_token_length=4,
                header_code=method_map[method.upper()],
                header_mid=1337,
                token=b"1234",
                options={CoapOption.URI_PATH: path.encode()},
                payload=data.encode() if data else b"",
            )

            logger.debug(f"CoAP Request: {coap_request}")

            sock.sendto(encode_message(coap_request), (host, port))
            logger.info("Request sent, waiting for response...")

            response_data = sock.recv(1024)
            response = parse_message(response_data)

            logger.info(f"Response Code: {response.header_code}")
            logger.debug(f"Response Data: {response.payload.decode()}")

            typer.echo(f"Response Code: {response.header_code}")
            typer.echo(f"Data: {response.payload.decode()}")

    except socket.timeout:
        logger.error("Request timed out")
        typer.echo("Error: Request timed out", err=True)
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        typer.echo(f"Critical Error: {e}", err=True)


if __name__ == "__main__":
    app()
