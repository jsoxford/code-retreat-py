import logging
import json
import re
import socket


log = logging.getLogger('code-retreat')


class NoData(Exception):
    pass


def get_data(sock):
    """
    Get data from the socket

    Defensively try to get data from the socket.
    """
    if sock is None:
        sock = get_socket()
        if sock is None:
            # the server really doesn't want to respond
            log.debug('Couldn\'t create socket')
            raise NoData

    data = sock.recv(1024)
    log.debug('Data 1: {}'.format(data))
    if len(data) == 0:
        # socket is dead so try to connect again
        sock = get_socket()
        if sock is None:
            log.debug('Socket was dead. Failed to recreate it.')
            raise NoData

        data = sock.recv(1024)
        log.debug('Data 2: {}'.format(data))
        if len(data) == 0:
            # socket is dead again, bail out
            log.debug('Failed to receive data two versions of the socket.')
            raise NoData

    return data


def get_socket():
    """Create an INET, STREAMing socket"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('', 3001))
    except socket.error:
        log.debug('Failed to create socket.')
        return None

    return s


def send(sock, user_code):
    """Send return value of the user's function to the server"""
    data = get_data(sock)

    # It's is alive!
    info = json.loads(data.split('\n')[0])
    log.debug('Parsed: {}'.format(info))

    iteration, coords = info['payload'].items()[0]
    next_step = user_code.get_next_step(coords)

    next_iteration = 'g{}'.format(int(iteration.split('g')[1]) + 1)

    # build response
    response = json.dumps({
        'respondingTo': 'processIteration',
        'payload': {
            iteration: coords,
            next_iteration: next_step,
        }
    })

    log.debug('Sending: {}'.format(response))

    sock.sendall(response)
