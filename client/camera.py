from constants import SCREEN


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.prev_x, self.prev_y = 0, 0
        self.curr_x, self.curr_y = None, None

    def apply(self):
        return self.curr_x, self.curr_y

    def update(self, target, mouse_pos):
        a, b = SCREEN.WINDOW_WIDTH // 2 - mouse_pos[0], SCREEN.WINDOW_HEIGHT // 2 - mouse_pos[1]
        self.dx = -(target.rect.x + target.rect.w // 2 - SCREEN.WINDOW_WIDTH // 2 - a // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - SCREEN.WINDOW_HEIGHT // 2 - b // 2)
        if self.curr_x is None:
            self.curr_x, self.curr_y = self.dx, self.dy
        else:
            self.curr_x += (self.dx - self.curr_x) / 30
            self.curr_y += (self.dy - self.curr_y) / 30
