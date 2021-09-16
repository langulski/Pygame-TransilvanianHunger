import pygame as pg


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = 800
        self.height = 600

    def apply(self, entity):
         return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(200 / 2)
        y = -target.rect.y + int(300 / 2)

            # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
