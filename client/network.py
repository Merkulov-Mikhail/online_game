import socket
import json
from constants import NETWORK


def key_required(func):
    def __wrapper(*args, **kwargs):
        if args[0]._key is None:
            print("Key hasn't been set!")
            return
        return func(*args, **kwargs)

    return __wrapper


class Network:
    def __init__(self, address=None, port=None):
        if address is None:
            self._conn = socket.create_connection(address=(NETWORK.ADDRESS, NETWORK.PORT))
        else:
            if port is None:
                self._conn = socket.create_connection(address=(address, NETWORK.PORT))
            else:
                self._conn = socket.create_connection(address=(address, port))
        self._get_and_set_key()

    def _get_and_set_key(self):
        r = self._conn.recv(1024).decode(encoding='utf-8')
        self._key = json.loads(r)[NETWORK.AUTH_STRING]

    @key_required
    def send_data(self, message_type, *args, **kwargs):
        dat = {NETWORK.AUTH_STRING: self._key}
        if message_type == NETWORK.CONTENT_TYPES.UPDATE:
            dat["type"] = NETWORK.CONTENT_TYPES.UPDATE
            dat["events"] = kwargs["events"]
            dat["angle"] = kwargs["angle"]
        self._conn.send(bytes(json.dumps(dat), encoding='utf-8'))

    @key_required
    def receive_data(self, amount=1024):
        try:
            ans = self._conn.recv(amount)
        except OSError:
            print("Connection to server lost")
            return None
        try:
            dat = json.loads(ans)
        except json.decoder.JSONDecodeError:
            print("Incorrect server answer")
            return None
        return dat
