#!/usr/bin/env python3

"""
A CLI tool to send CoAP requests, similarly to the curl.
Uses external aiocoap library.
"""

import asyncio
from urllib.parse import urlparse

import aiocoap
import typer

app = typer.Typer()


async def async_request(method: str, uri: str, data: str | None = None):
    """Async handler for CoAP requests"""

    # Create context
    context = await aiocoap.Context.create_client_context()

    # Build request
    request = aiocoap.Message(
        code=getattr(aiocoap.Code, method),
        uri=uri,
        payload=data.encode() if data else b"",
    )

    try:
        response = await context.request(request).response
        return response
    except Exception as e:
        typer.echo(f"Failed to fetch resource: {e}")
        raise typer.Exit(1)
    finally:
        await context.shutdown()


@app.command()
def request(
    method: str = typer.Option(
        "GET", help="CoAP method (GET/POST/PUT/DELETE)"
    ),
    uri: str = typer.Argument(..., help="CoAP URI (coap://host:port/path)"),
    data: str = typer.Option(None, help="Data to send in request body"),
):
    """Send CoAP request to server"""

    # Validate URI scheme
    parsed_uri = urlparse(uri)
    if parsed_uri.scheme != "coap":
        raise typer.BadParameter("URI must use coap:// scheme")

    # Run async request
    response = asyncio.run(async_request(method.upper(), uri, data))

    # Print response
    typer.echo(f"Response Code: {response.code}")
    typer.echo(f"Data: {response.payload.decode()}")


if __name__ == "__main__":
    app()
