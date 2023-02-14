import pygame
import random
from constants import PLAYER, ENTITIES, EVENTS


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
        self.sprinting = False
        self.diagonal_movement = False

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

    def key_pressed(self, key):
        if key == EVENTS.KEY_SHIFT:
            self.sprinting = True

    def modification(self, ev):
        if ev == EVENTS.DIAGONAL_MOVEMENT:
            self.diagonal_movement = True

    def __str__(self):
        return f"{ENTITIES.PLAYER_ID};{self.rect.x};{self.rect.y};{self.angle};{self.health}"

    def __repr__(self):
        return f"{ENTITIES.PLAYER_ID};{self.rect.x};{self.rect.y};{self.angle};{self.health}"
