import os
import random

from serverEntities import Server_Obstacle


class Level:
    def __init__(self, width, height):
        self.width, self.height = width, height
        Server_Obstacle(0, 0, width, height, fill=1)
        self.clusters = random.randint(3, 20)
        for _ in range(self.clusters):
            self.generate_cluster(random.randint(0, width), random.randint(0, height))

    def generate_cluster(self, x, y):
        self.generate_structure(x, y)

    def generate_structure(self, x, y):
        offset_x = random.randint(-200, 200)
        offset_y = random.randint(-200, 200)
        if not os.listdir("structures"):
            return
        struc = random.choice(os.listdir("structures"))
        dat = open(f"structures/{struc}", mode="r").read().split("\n")
        mult = random.randint(-10, 100)
        k = 1 + mult / 100
        for rect in dat:
            if not rect:
                continue
            struc_x, struc_y, w, h = map(int, rect.split(";"))
            Server_Obstacle(x=x + offset_x + struc_x * k, y=y + offset_y + struc_y * k, width=w * k, height=h * k)
