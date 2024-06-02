import pygame
import math
from constants import PLAYER, COLORS, SCREEN, EVENTS, NETWORK, ENTITIES, BULLET
from client.network import Network
from client.camera import Camera


camera = Camera()
screen = pygame.display.set_mode((SCREEN.WINDOW_WIDTH, SCREEN.WINDOW_HEIGHT))
all_sprites = pygame.sprite.Group()
collision_sprites = pygame.sprite.Group()
game_status = False


class Player(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__(all_sprites)
        self.sprinting = False
        self.shooting = 3
        self.events = list()
        self.rect = pygame.Rect(x, y, PLAYER.PLAYER_SIZE, PLAYER.PLAYER_SIZE)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            self.events.append(EVENTS.KEY_SHIFT)

        if self.shooting == 1:
            self.events.append(EVENTS.LEFT_MOUSE_DOWN)
        elif self.shooting == 2:
            self.shooting = 3
            self.events.append(EVENTS.LEFT_MOUSE_UP)

        if (keys[pygame.K_w] and (keys[pygame.K_a] or keys[pygame.K_d])) or \
                (keys[pygame.K_s] and (keys[pygame.K_a] or keys[pygame.K_d])):
            self.events.append(EVENTS.DIAGONAL_MOVEMENT)

        if keys[pygame.K_w]:
            self.events.append(EVENTS.UP)

        if keys[pygame.K_s]:
            self.events.append(EVENTS.DOWN)

        # x value changing
        if keys[pygame.K_a]:
            self.events.append(EVENTS.LEFT)

        if keys[pygame.K_d]:
            self.events.append(EVENTS.RIGHT)


def main():
    pl = Player()
    all_sprites.add(pl)
    clock = pygame.time.Clock()
    net = Network()
    mouse_position = 0, 0
    camera.update(pl, mouse_position)
    while True:
        screen.fill(COLORS.DARKNESS_COLOR)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return
            if ev.type == pygame.MOUSEMOTION:
                mouse_position = ev.pos
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    pl.shooting = 1     # started shooting
            if ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:
                    pl.shooting = 2     # Stopped shooting
        angle = calculate_angle(pl, mouse_position)
        net.send_data(message_type=NETWORK.CONTENT_TYPES.UPDATE, events=pl.events, angle=angle)
        camera.update(pl, mouse_position)
        pl.events.clear()
        obj = net.receive_data()
        if obj is not None:
            if obj['type'] == NETWORK.CONTENT_TYPES.UPDATE:
                for entity in obj['entities']:
                    draw_entity(screen, list(map(float, entity.split(';'))))
                dat = obj['state'].split(';')
                pl.rect.x = float(dat[1])
                pl.rect.y = float(dat[2])

        pl.update()
        pygame.display.flip()
        clock.tick(60)


def loading_screen():
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONUP:
                print(ev.pos)

        pygame.display.flip()


def calculate_angle(player, cursor):
    x, y = normalize(player.rect.x + PLAYER.PLAYER_SIZE / 2, player.rect.y + PLAYER.PLAYER_SIZE / 2)
    x1, y1 = cursor[0], cursor[1]
    ab = abs(y1 - y)
    ac = abs(x1 - x)
    try:
        angle = math.atan(ab / ac) / math.pi * 180
    except ZeroDivisionError:
        angle = 0
    if x > x1 and y > y1:
        return 180 - angle
    if x > x1 and y < y1:
        return 180 + angle
    if x < x1 and y > y1:
        return angle
    if x < x1 and y < y1:
        return 360 - angle
    return angle


def draw_entity(sc, ent):
    typ = ent[0]
    new_x, new_y = normalize(ent[1], ent[2])
    if typ == ENTITIES.PLAYER_ID:
        # If player is dead, we do not show him
        if int(ent[4]) == 0:
            return
        pygame.draw.ellipse(sc, COLORS.PLAYER_BORDER, (new_x, new_y, PLAYER.PLAYER_SIZE, PLAYER.PLAYER_SIZE))
        pygame.draw.ellipse(sc, COLORS.PLAYER_BODY, (new_x + PLAYER.PLAYER_SIZE * 0.1, new_y + PLAYER.PLAYER_SIZE * 0.1,
                                                     PLAYER.PLAYER_SIZE * 0.8, PLAYER.PLAYER_SIZE * 0.8))
        ang = ent[3] + 45
        radius = 0.3 * PLAYER.PLAYER_SIZE
        pygame.draw.ellipse(sc, COLORS.PLAYER_EYES,
                            (new_x + PLAYER.PLAYER_SIZE / 2 + math.sin(ang * math.pi / 180) * radius - PLAYER.PLAYER_EYES_RADIUS,
                             new_y + PLAYER.PLAYER_SIZE / 2 + math.cos(ang * math.pi / 180) * radius - PLAYER.PLAYER_EYES_RADIUS,
                             PLAYER.PLAYER_EYES_RADIUS * 2,
                             PLAYER.PLAYER_EYES_RADIUS * 2))
        pygame.draw.ellipse(sc, COLORS.PLAYER_EYES,
                            (new_x + PLAYER.PLAYER_SIZE / 2 + math.sin((ang + 90) * math.pi / 180) * radius - PLAYER.PLAYER_EYES_RADIUS,
                             new_y + PLAYER.PLAYER_SIZE / 2 + math.cos((ang + 90) * math.pi / 180) * radius - PLAYER.PLAYER_EYES_RADIUS,
                             PLAYER.PLAYER_EYES_RADIUS * 2,
                             PLAYER.PLAYER_EYES_RADIUS * 2))
    if typ == ENTITIES.BULLET_ID:
        pygame.draw.ellipse(sc, COLORS.BULLET,
                            (new_x, new_y, BULLET.BULLET_SIZE, BULLET.BULLET_SIZE))
    if typ == ENTITIES.OBSTACLE_ID:
        pygame.draw.rect(sc, COLORS.WHITE,
                         (new_x, new_y, ent[3], ent[4]))


def normalize(x, y):
    a, b = camera.apply()
    return x + a, y + b


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
    exit()
