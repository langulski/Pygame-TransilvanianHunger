import pygame as pg
import sys
from settings import *
from level import Level


pg.init()
display = pg.Surface((600, 400))
screen = pg.display.set_mode((screen_width,screen_height))
clock = pg.time.Clock()
tile_size = 64
level = Level(level_map,screen)



while True:
    for event in pg.event.get():
        if event.type ==pg.QUIT:
            pg.quit()
            sys.exit()
    

    
    screen.fill((51, 51, 0))
    level.run()

    pg.display.update()
    clock.tick (60)
               