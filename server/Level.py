import pygame
from serverEntities import Server_Obstacle


class Level:
    def __init__(self, width, height):
        Server_Obstacle(0, 0, width, height, fill=1)