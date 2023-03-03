import pygame
import math
import random
from constants import PLAYER, ENTITIES, EVENTS, BULLET


class Server_Player(pygame.sprite.Sprite):
    """
    Represents every player on stage
    """
    def __init__(self, x, y, angle=90, health=100, gr=None):
        if gr is not None:
            super().__init__(gr)
        else:
            super().__init__()
        self.rect = pygame.Rect(x, y, PLAYER.PLAYER_SIZE, PLAYER.PLAYER_SIZE)
        self.angle = random.randint(0, 360)
        self.health = health
        self.shooting = False
        self.sprinting = False
        self.diagonal_movement = False
        self.prev_fire_tick = -2

    def move(self, direction, collision_objects):
        if self.sprinting:
            val = PLAYER.MOVEMENT_SPEED * PLAYER.SPRINT_MULTIPLIER
        else:
            val = PLAYER.MOVEMENT_SPEED
        if self.diagonal_movement:
            val *= PLAYER.DIAGONAL_MULTIPLIER
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
            if pygame.sprite.spritecollideany(self, collision_objects):
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

    def take_damage(self):
        return

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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, gr=None):
        if gr is not None:
            super().__init__(gr)
        else:
            super().__init__()
        self.rect = pygame.Rect(x + PLAYER.PLAYER_SIZE / 2, y + PLAYER.PLAYER_SIZE / 2, BULLET.BULLET_SIZE, BULLET.BULLET_SIZE)
        self.angle = angle
        self.spawn_point = x + PLAYER.PLAYER_SIZE / 2, y + PLAYER.PLAYER_SIZE / 2
        self.can_damage = False

    def id(self):
        return ENTITIES.BULLET_ID

    def move(self):
        self.rect.x += math.cos((-self.angle) * math.pi / 180) * BULLET.BULLET_SPEED
        self.rect.y += math.sin((-self.angle) * math.pi / 180) * BULLET.BULLET_SPEED

    def __str__(self):
        return f"{ENTITIES.BULLET_ID};{self.rect.x};{self.rect.y};{self.angle}"

    def __repr__(self):
        return f"{ENTITIES.BULLET_ID};{self.rect.x};{self.rect.y};{self.angle}"
