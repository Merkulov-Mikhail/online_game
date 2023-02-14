import pygame
import math
from constants import PLAYER, COLORS, GEOMETRY, SCREEN, EVENTS, NETWORK, ENTITIES
from network import Network


screen = pygame.display.set_mode((SCREEN.WINDOW_WIDTH, SCREEN.WINDOW_HEIGHT))
all_sprites = pygame.sprite.Group()
collision_sprites = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y
        self.sprinting = False
        self.events = list()
        self.rect = pygame.Rect(self.x, self.y, PLAYER.PLAYER_SIZE, PLAYER.PLAYER_SIZE)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            self.sprinting = True
            self.events.append(EVENTS.KEY_SHIFT)

        if self.sprinting:
            val = PLAYER.MOVEMENT_SPEED * PLAYER.SPRINT_MULTIPLIER
        else:
            val = PLAYER.MOVEMENT_SPEED

        if keys[pygame.K_w] and (keys[pygame.K_a] or keys[pygame.K_d]):
            self.events.append(EVENTS.DIAGONAL_MOVEMENT)
        elif keys[pygame.K_s] and (keys[pygame.K_a] or keys[pygame.K_d]):
            self.events.append(EVENTS.DIAGONAL_MOVEMENT)

        # y value changing
        if keys[pygame.K_w]:
            self.events.append(EVENTS.UP)
            self.rect.y -= val
            if pygame.sprite.spritecollideany(self, collision_sprites):
                self.rect.y += val

        if keys[pygame.K_s]:
            self.events.append(EVENTS.DOWN)
            self.rect.y += val
            if pygame.sprite.spritecollideany(self, collision_sprites):
                self.rect.y -= val

        # x value changing
        if keys[pygame.K_a]:
            self.events.append(EVENTS.LEFT)
            self.rect.x -= val
            if pygame.sprite.spritecollideany(self, collision_sprites):
                self.rect.x += val

        if keys[pygame.K_d]:
            self.events.append(EVENTS.RIGHT)
            self.rect.x += val
            if pygame.sprite.spritecollideany(self, collision_sprites):
                self.rect.x -= val

    def mouse_move(self, pos):
        x1, y1 = pos[0], 0
        x2, y2 = pos[0] - self.rect.x, pos[1] - self.rect.y
        print(x1, y1, x2, y2)


def main():
    pl = Player()
    all_sprites.add(pl)
    clock = pygame.time.Clock()
    net = Network()
    while True:
        screen.fill(COLORS.DARKNESS_COLOR)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return
            if ev.type == pygame.MOUSEMOTION:
                pl.mouse_move(ev.pos)
        net.send_data(message_type=NETWORK.CONTENT_TYPES.UPDATE, events=pl.events)
        pl.events.clear()
        obj = net.receive_data()
        if obj['type'] == NETWORK.CONTENT_TYPES.UPDATE:
            for entity in obj['entities']:
                draw_entity(screen, list(map(int, entity.split(';'))))
        pl.update()
        pygame.display.flip()
        clock.tick(60)


def draw_entity(sc, ent):
    typ = ent[0]
    if typ == ENTITIES.PLAYER_ID:
        pygame.draw.ellipse(sc, COLORS.PLAYER_BODY, (ent[1], ent[2], PLAYER.PLAYER_SIZE, PLAYER.PLAYER_SIZE))
        ang = ent[3]
        x1, y1 = PLAYER.PLAYER_SIZE / 2 + ent[1], PLAYER.PLAYER_SIZE / 2 + ent[2]
        pygame.draw.ellipse(sc, COLORS.PLAYER_EYES,
                            (x1 + 0.25 * PLAYER.PLAYER_SIZE * math.sin((ang - 100) * math.pi / 180),
                             y1 + 0.25 * PLAYER.PLAYER_SIZE * math.cos((ang - 30) * math.pi / 180),
                             PLAYER.PLAYER_EYES_SIZE,
                             PLAYER.PLAYER_EYES_SIZE))
        pygame.draw.ellipse(sc, COLORS.PLAYER_EYES,
                            (x1 + 0.25 * PLAYER.PLAYER_SIZE * math.sin((ang + 30) * math.pi / 180),
                             y1 + 0.25 * PLAYER.PLAYER_SIZE * math.cos((ang + 30) * math.pi / 180),
                             PLAYER.PLAYER_EYES_SIZE,
                             PLAYER.PLAYER_EYES_SIZE))


pygame.init()
main()
pygame.quit()
exit()