import socket
from urllib.parse import urlparse

import typer

from coap_server.utils.constants import CoapCode, CoapMessage, CoapOption
from coap_server.utils.parser import encode_message, parse_message

app = typer.Typer()


@app.command()
def request(
    method: str = typer.Option(
        "GET", help="HTTP method (GET/POST/PUT/DELETE)"
    ),
    uri: str = typer.Argument(..., help="CoAP URI (coap://host:port/path)"),
    data: str = typer.Option(None, help="Data to send in request body"),
):
    """Send CoAP request to server"""

    # Parse URI
    parsed_uri = urlparse(uri)
    if parsed_uri.scheme != "coap":
        raise typer.BadParameter("URI must use coap:// scheme")

    host = parsed_uri.hostname
    port = parsed_uri.port or 5683
    path = parsed_uri.path

    # Map method string to CoapCode enum
    method_map = {
        "GET": CoapCode.GET,
        "POST": CoapCode.POST,
        "PUT": CoapCode.PUT,
        "DELETE": CoapCode.DELETE,
    }

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        coap_request = CoapMessage(
            header_version=1,
            header_type=0,
            header_token_length=4,
            header_code=method_map[method.upper()],
            header_mid=1337,
            token=b"1234",
            options={
                CoapOption.URI_PATH: path.encode(),
            },
            payload=data.encode() if data else b"",
        )

        print(coap_request)

        sock.sendto(encode_message(coap_request), (host, port))
        response_data = sock.recv(1024)
        response = parse_message(response_data)
        typer.echo(f"Response Code: {response.header_code}")
        typer.echo(f"Data: {response.payload.decode()}")


if __name__ == "__main__":
    app()
