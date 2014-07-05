import socket

from code_retreat.server import get_socket


def test_get_socket_address():
    pass


def test_get_socket():
    sock = get_socket()
    assert type(sock) == socket.SocketType
