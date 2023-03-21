import pygame


def load_image(name):
    import os
    print(os.getcwd() + name)
    if os.path.isfile(name):
        return pygame.image.load(name)
    else:
        raise "Adslkjsjdfos;jdt"


class Over(pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = load_image("data/game over.png")
        self.p = 1
        self.mod = 1.1
        self.rect = self.image.get_rect()
        self.rect.x = -600

    def update(self):
        self.rect.x += self.p * 1 * self.mod
        x = self.rect.x
        if x == 0:
            self.p = 0


fps = 60
pygame.init()
screen = pygame.display.set_mode((600, 300))
sprites = pygame.sprite.Group()
sprites.add(Over())
running = True
clock = pygame.time.Clock()
screen.fill("#0000ff")
while running:
    for ev in pygame.event.get():
        if ev == pygame.KEYDOWN:
            running = False
    screen.fill("#000000")
    sprites.update()
    sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()