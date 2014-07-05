import logging
import json
import socket

import requests


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

    data = sock.recv(4096)
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
    """
    Create a socket to the GoL Server

    The IP is retrieved from a JSON document hosted at jsoxford.com to avoid
    IP changing issues on networks we can't control.
    """
    url = 'http://jsoxford.com/cr.json'
    r = requests.get(url)
    if not r.ok:
        log.debug('Could not get server address data: {}'.format(r.status_code))
        return None

    address = tuple(r.json()['endpoint'].values())

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(address)
    except socket.error:
        log.debug('Failed to create socket.')
        return None

    log.debug('Socket connected to: {}:{}'.format(*address))
    return s


def send(sock, user_code):
    """Send return value of the user's function to the server"""
    data = get_data(sock)

    # It's is alive!
    info = json.loads(data.split('\n')[0])
    log.debug('Parsed: {}'.format(info))

    generation = info['payload']['generation']
    result = info['payload']['results']
    user_result = user_code.tickBoard(result)

    # build response
    response = json.dumps({
        'status': '',
        'respondingTo': 'tickBoard',
        'payload': [{
            'generation': generation,
            'result': result,
        }, {
            'generation': generation + 1,
            'result': user_result,
        }]
    })

    log.debug('Sending: {}'.format(response))

    sock.sendall(response)
