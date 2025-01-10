import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    server_address = ("127.0.0.1", 5683)
    version = 1
    type = 2
    tkl = 3
    class_ = 4
    code = 5
    mid = 12345

    header = (version << 6) | (type << 4) | (tkl << 0)
    header = (header << 8) | (class_ << 5) | (code << 0)
    header = (header << 16) | mid

    sock.sendto(header.to_bytes(4, byteorder="big"), server_address)