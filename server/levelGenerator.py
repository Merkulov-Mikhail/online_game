import pygame
import sys
import os
from serverEntities import collision_sprites, Server_Obstacle


class Level:
    def __init__(self, height, width, seed=None, **meta):
        """
        :param height:
        :param width:
        :param meta:
        """
        import random
        if seed is not None:
            random.seed(seed)
        else:
            random.seed(random.randint(1, int(1e18)))
        Server_Obstacle(0, 0, width=width, height=height, fill=0, gr=collision_sprites)
        self.choose_structure()

    def choose_structure(self):
        print(os.listdir("structures"))
