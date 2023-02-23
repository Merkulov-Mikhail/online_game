import socket
import json
from constants import NETWORK
from threading import Thread
from random import randint
from hashlib import sha256
from serverEntities import *


all_events = []
collision_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
for ev in EVENTS.__dict__:
    if type(EVENTS.__dict__[ev]) == int:
        all_events.append(EVENTS.__dict__[ev])


def create_key():
    return sha256(bytes(randint(int(5e5), int(1e6))))


class Server:
    def __init__(self):
        self._running = True
        self._connections = {}

    def _connection(self, connection, address):
        print(f"[INFO] Successfully created connection with {address}!")
        cnt = 0
        while True:
            try:
                response = connection.recv(1024 * 2 ** 4)
                data = json.loads(response.decode(encoding='utf-8'))
            except json.decoder.JSONDecodeError:
                print(f"[WARNING] Got incorrect user({address[0]}) response: {response}")
                cnt += 1
                if cnt == 10:
                    break
                continue
            except Exception as e:
                print(f"[WARNING] Error while receiving data from user ({e})")
                cnt += 1
                if cnt == 10:
                    break
                continue
            key = self._update(json_data=data)

            all_sprites_package = {"type": NETWORK.CONTENT_TYPES.UPDATE, "entities": [], "state": str(self._connections[key])}
            for value in self._connections.values():
                all_sprites_package["entities"].append(str(value))
            try:
                connection.send(bytes(json.dumps(all_sprites_package), encoding='utf-8'))
            except Exception as e:
                print(f"[ERROR] An error acquired while sending data to {address[0]}")
                print(e)
                cnt += 1
                if cnt == 10:
                    break
            cnt = 0

        print(f"[INFO] Breaking connection with {address}")
        return

    def _update(self, json_data: dict):
        if NETWORK.AUTH_STRING not in json_data:
            return
        if json_data[NETWORK.AUTH_STRING] not in self._connections:  # if key is not correct
            return
        key = json_data[NETWORK.AUTH_STRING]
        if NETWORK.CONTENT_TYPES.UPDATE == json_data["type"]:
            self._connections[key].angle = json_data["angle"]
            current_events = set(json_data["events"])
            for ev in all_events:
                if ev in current_events:
                    if ev // 100 == EVENTS.DIRECTIONS // 100:
                        self._connections[key].move(ev, collision_sprites)
                    if ev // 100 == EVENTS.KEYS // 100:
                        self._connections[key].key_pressed(ev)
                    if ev // 100 == EVENTS.SPECIAL_MODIFICATIONS // 100:
                        self._connections[key].modification(ev)
            self._connections[key].sprinting = False
            self._connections[key].diagonal_movement = False
        return key

    def authentication(self, con, ad):
        while key := create_key().hexdigest():
            if key not in self._connections:
                self._connections[key] = Server_Player(0, 0)  # TODO rework this shit
                break
        package = {"type": NETWORK.CONTENT_TYPES.AUTH, NETWORK.AUTH_STRING: key}
        con.send(bytes(json.dumps(package), encoding='utf-8'))
        _ = Thread(target=self._connection, args=(con, ad))
        _.start()

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind((NETWORK.ADDRESS, NETWORK.PORT))
        except socket.error as e:
            print(e)
        print(sock)
        sock.listen()
        print("Waiting for a connection, Server Started")
        while self._running:
            conn, addr = sock.accept()
            print(f"[CONNECT] New connection from {addr}!")
            self.authentication(conn, addr)


if __name__ == '__main__':
    a = Server()
    a.start()
