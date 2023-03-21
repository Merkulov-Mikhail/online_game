import pygame
import math
from constants import PLAYER, ENTITIES, EVENTS, BULLET


collision_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


class Server_Player(pygame.sprite.Sprite):
    """
    Represents every player on stage
    """
    def __init__(self, x, y, angle=90, health=100, gr=None):
        if gr is not None:
            super().__init__(all_sprites, gr)
        else:
            super().__init__(all_sprites)

        self.rect = pygame.Rect(x, y, PLAYER.PLAYER_SIZE, PLAYER.PLAYER_SIZE)
        self.angle = angle
        self.health = health
        self.shooting = False
        self.sprinting = False
        self.diagonal_movement = False
        self.prev_fire_tick = -2

    def move(self, direction, collision_objects):
        if self.sprinting:
            val = int(PLAYER.MOVEMENT_SPEED * PLAYER.SPRINT_MULTIPLIER)
        else:
            val = PLAYER.MOVEMENT_SPEED
        if self.diagonal_movement:
            val = int(val * PLAYER.DIAGONAL_MULTIPLIER)
        if direction == EVENTS.UP:
            self.rect.y -= val
            if pygame.sprite.spritecollideany(self, collision_objects):
                self.rect.y += val
        if direction == EVENTS.DOWN:
            self.rect.y += val
            if pygame.sprite.spritecollideany(self, collision_objects):
                self.rect.y -= val

        if direction == EVENTS.LEFT:
            self.rect.x -= val
            if pygame.sprite.spritecollideany(self, collision_objects):
                self.rect.x += val
        if direction == EVENTS.RIGHT:
            self.rect.x += val
            if sp:=pygame.sprite.spritecollideany(self, collision_objects):
                self.rect.x -= val

    def fire(self, tick, fire_rate):
        if self.shooting and tick - self.prev_fire_tick >= fire_rate:
            self.prev_fire_tick = tick
            return True
        return False

    def key_pressed(self, key):
        if key == EVENTS.KEY_SHIFT:
            self.sprinting = True
        if key == EVENTS.LEFT_MOUSE_DOWN:
            self.shooting = True
        if key == EVENTS.LEFT_MOUSE_UP:
            self.shooting = False

    def take_damage(self, damage_value):
        self.health -= damage_value
        self.health = max(0, self.health)

    def is_alive(self):
        return bool(self.health)

    def get_cords(self):
        return self.rect.x, self.rect.y

    def modification(self, ev):
        if ev == EVENTS.DIAGONAL_MOVEMENT:
            self.diagonal_movement = True

    def id(self):
        return ENTITIES.PLAYER_ID

    def __str__(self):
        return f"{ENTITIES.PLAYER_ID};{self.rect.x};{self.rect.y};{self.angle};{self.health}"

    def __repr__(self):
        return f"{ENTITIES.PLAYER_ID};{self.rect.x};{self.rect.y};{self.angle};{self.health}"


class Server_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, damage=BULLET.BASIC_BULLET_DAMAGE, gr=None):
        if gr is not None:
            super().__init__(gr)
        else:
            super().__init__()
        self._damage = damage
        self.rect = pygame.Rect(x + PLAYER.PLAYER_SIZE / 2, y + PLAYER.PLAYER_SIZE / 2, BULLET.BULLET_SIZE, BULLET.BULLET_SIZE)
        self.angle = angle
        self.spawn_point = x + PLAYER.PLAYER_SIZE / 2, y + PLAYER.PLAYER_SIZE / 2
        self.can_damage = False
        self.last_move = 0

    def id(self):
        return ENTITIES.BULLET_ID

    def get_damage(self):
        return self._damage

    def move(self):
        self.rect.x += math.cos((-self.angle) * math.pi / 180) * BULLET.BULLET_SPEED
        self.rect.y += math.sin((-self.angle) * math.pi / 180) * BULLET.BULLET_SPEED

    def __str__(self):
        return f"{ENTITIES.BULLET_ID};{self.rect.x};{self.rect.y};{self.angle}"

    def __repr__(self):
        return f"{ENTITIES.BULLET_ID};{self.rect.x};{self.rect.y};{self.angle}"


class Server_Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, gr=None, fill=0):
        if fill:
            Server_Obstacle(x, y, 10, height, gr=gr)
            Server_Obstacle(x, y, width, 10, gr=gr)
            Server_Obstacle(x + width, y, 10, height, gr=gr)
            Server_Obstacle(x, y + height, width, 10, gr=gr)
            del self
            return
        if gr is not None:
            super().__init__(all_sprites, collision_sprites, gr)
        else:
            super().__init__(all_sprites, collision_sprites)

        self.rect = pygame.Rect(x, y, width, height)

    def id(self):
        return ENTITIES.OBSTACLE_ID

    def __str__(self):
        return f"{self.id()};{self.rect.x};{self.rect.y};{self.rect.w};{self.rect.h}"

    def __repr__(self):
        return f"{self.id()};{self.rect.x};{self.rect.y};{self.rect.w};{self.rect.h}"
