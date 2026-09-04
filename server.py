import socket


HOST = "0.0.0.0"
PORT = 5000


def start_server() -> None:
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )

    server_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1,
    )

    server_socket.bind(
        (HOST, PORT)
    )

    server_socket.listen(1)

    print(
        f"Server started. Listening on port {PORT}..."
    )

    client_socket, client_address = (
        server_socket.accept()
    )

    print(
        f"Client connected: {client_address}"
    )

    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    start_server()