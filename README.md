# CoAP Server

A lightweight CoAP server implementation supporting essential request methods.

## Features

- Supports `GET`, `POST`, `PUT`, and `DELETE` requests.
- Returns appropriate response codes following [RFC 7252](https://datatracker.ietf.org/doc/html/rfc7252) specification.
- Logs all server events, including request details and errors.
- Organizes data in a hierarchical resource structure with unique URLs.
- Handles multiple clients simultaneously with efficient performance.

## Use Cases

This server is designed to process requests within an IoT network. Example use cases include:

- `GET`: Retrieve the current temperature from a sensor.
- `POST`: Register a new sensor.
- `PUT`: Update a sensor's temperature.
- `DELETE`: Remove a sensor.

## Error Handling

The server returns appropriate error codes based on the [RFC 7252](https://datatracker.ietf.org/doc/html/rfc7252) specification:

- `4.xx` – Client-side errors (e.g., bad request, unauthorized access).
- `5.xx` – Server-side errors (e.g., internal server failure, unavailable resource).

All errors are logged with timestamps, client IP addresses, request URLs, and response codes.

## Tech Stack

- **Operating System:** GNU/Linux (tested on Ubuntu 24.04 and openSUSE Tumbleweed)
- **Containerization:** Docker, Docker Compose
- **Programming Language:** Python 3.11
- **Package Management:** Poetry
- **Linter & Formatter:** Ruff
- **Static Analysis:** Mypy
- **Testing:** Pytest

## Architecture

The server is containerized using Docker to simulate the system architecture. Individual containers represent different components and communicate over a Docker network.

### API Functional Blocks

- **Server Initialization** – Bootstraps the application and sets up necessary configurations.
- **Listening for Requests** – Handles incoming CoAP requests.
- **Request Processing** – Responds to `GET`, `POST`, `PUT`, and `DELETE` requests.

## Testing

- **Unit Tests** – Ensures core functionality is reliable.
- **Integration Tests** – Validates client-server communication and system stability.
- **Manual Tests** – Conducted with documented test cases.

## Getting Started

### Prerequisites

- Python 3.11
- Poetry for package management
- Docker (optional)

### Installation

#### Using Docker

1. Clone the repository:
   ```sh
   git clone https://github.com/maksnowak/CoAPServer
   cd CoAPServer
   ```
2. Build the image:
   ```sh
   docker build -t coap_server .
   ```
3. Run the container:
   ```sh
   docker run -p 5683:5683 coap_server
   ```

#### Locally, using Poetry

1. Clone the repository:
   ```sh
   git clone https://github.com/maksnowak/CoAPServer
   cd CoAPServer
   ```
2. Install dependencies:
   ```sh
   make install
   ```
3. Start the server:
   ```sh
   make run
   ```

## License

This project is open-source and available under the [GNU GPLv3 License](LICENSE).
