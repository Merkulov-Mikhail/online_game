import socket
import json

import pygame.time
from levelGenerator import Level
from constants import NETWORK, GUNS
from threading import Thread
from random import randint
from hashlib import sha256
from serverEntities import *


game_config = [0]
all_events = []
players = pygame.sprite.Group()
bullets = pygame.sprite.Group()
for ev in EVENTS.__dict__:
    if type(EVENTS.__dict__[ev]) == int:
        all_events.append(EVENTS.__dict__[ev])


def create_key():
    return sha256(bytes(randint(int(5e5), int(1e6))))


def log_print(dat):
    f = open("log.txt", "a")
    f.write(dat + "\n")
    f.close()


class Server:
    def __init__(self):
        self._running = True
        self._connections = {}

    def _connection(self, connection, address):
        log_print(f"[INFO] Successfully created connection with {address}!")
        cnt = 0
        while True:
            try:
                response = connection.recv(1024 * 2 ** 4)
            except Exception as e:
                log_print(f"[WARNING] Error in connection {e}")
                cnt += 1
                if cnt == 10:
                    break
                continue
            try:
                data = json.loads(response.decode(encoding='utf-8'))
            except json.decoder.JSONDecodeError:
                log_print(f"[WARNING] Got incorrect user({address[0]}) response: {response}")
                cnt += 1
                if cnt == 10:
                    break
                continue
            except Exception as e:
                log_print(f"[WARNING] Error while receiving data from user ({e})")
                cnt += 1
                if cnt == 10:
                    break
                continue
            key = self._update(json_data=data)
            all_sprites_package = {"type": NETWORK.CONTENT_TYPES.UPDATE, "entities": [], "state": str(self._connections[key])}
            for value in all_sprites:
                all_sprites_package["entities"].append(str(value))
            for bul in bullets:
                bul: Server_Bullet
                bul.move()
                if abs(bul.rect.x) >= 90000:
                    bullets.remove(bul)
                    continue
                if abs(bul.rect.y) >= 90000:
                    bullets.remove(bul)
                    continue
                sprite = pygame.sprite.spritecollideany(bul, all_sprites)
                # sprite can be None or a class from serverSprites
                if sprite:
                    if sprite.id() == ENTITIES.BULLET_ID:
                        sprite: Server_Bullet
                        bullets.remove(bul)
                        bullets.remove(sprite)
                        all_sprites.remove(sprite)
                    if sprite.id() == ENTITIES.PLAYER_ID:
                        sprite: Server_Player
                        if bul.can_damage:
                            sprite.take_damage(bul.get_damage())
                            if not sprite.is_alive():
                                all_sprites.remove(sprite)
                                players.remove(sprite)
                            bullets.remove(bul)
                    if sprite.id() == ENTITIES.OBSTACLE_ID:
                        bullets.remove(bul)
                else:
                    if not bul.can_damage:
                        bul.can_damage = True
                all_sprites_package["entities"].append(str(bul))
            try:
                connection.send(bytes(json.dumps(all_sprites_package), encoding='utf-8'))
            except Exception as e:
                log_print(f"[ERROR] An error acquired while sending data to {address[0]}")
                log_print(str(e))
                cnt += 1
                if cnt == 10:
                    break
            cnt = 0

        log_print(f"[INFO] Breaking connection with {address}")
        return

    def _update(self, json_data: dict):
        if NETWORK.AUTH_STRING not in json_data:
            return
        if json_data[NETWORK.AUTH_STRING] not in self._connections:  # if key is not correct
            return
        key = json_data[NETWORK.AUTH_STRING]
        if self._connections[key].is_alive():
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
            made_shot = self._connections[key].fire(game_config[0], GUNS.ASSAULT_RIFLE_FIRE_RATE)
            if made_shot:
                bul = Server_Bullet(*self._connections[key].get_cords(), angle=self._connections[key].angle)
                bullets.add(bul)
        return key

    def authentication(self, con, ad):
        while key := create_key().hexdigest():
            if key not in self._connections:
                self._connections[key] = Server_Player(10, 10, gr=players)  # TODO rework this shit
                break
        package = {"type": NETWORK.CONTENT_TYPES.AUTH, NETWORK.AUTH_STRING: key}
        con.send(bytes(json.dumps(package), encoding='utf-8'))
        _ = Thread(target=self._connection, args=(con, ad))
        _.start()

    def loop(self):
        """
        Game logic bases on ticks
        For example - fire rate depends on ticks, basic gun has delay of 1 tick, so every second tick player can shoot
        """
        cl = pygame.time.Clock()
        while True:
            game_config[0] += 1
            cl.tick(NETWORK.TPS)

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind((NETWORK.ADDRESS, NETWORK.PORT))
        except socket.error as e:
            log_print(str(e))
        print(sock)
        Level(randint(1400, 2000), randint(1400, 2000))
        sock.listen()
        _ = Thread(target=self.loop)
        _.start()
        print("Waiting for a connection, Server Started")
        while self._running:
            conn, addr = sock.accept()
            print(f"[CONNECT] New connection from {addr}!")
            self.authentication(conn, addr)

    def generate_level(self, width, height):
        Server_Obstacle(0, 0, width=width, height=height, fill=0, gr=collision_sprites)


if __name__ == '__main__':
    a = Server()
    a.start()
