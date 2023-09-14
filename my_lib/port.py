import socket
import random


def get_available_port():
    while True:
        port = random.randint(1024, 65535)  # generate random port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))  # bind port
                s.listen(1)  # listen
                return port  # return port
            except OSError:
                pass  # if port is occupied, try another one
