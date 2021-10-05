import pygame as pg
import sys
from settings import *
from level import Level
from gamedata import level_0



pg.init()
display = pg.Surface((400, 200))
WINDOW_SIZE = (screen_width,screen_height)
screen = pg.display.set_mode((screen_width,screen_height),0,32)
clock = pg.time.Clock()
level = Level(level_0,screen)



while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        
	
          
    
    level.run()

    pg.display.update()
    clock.tick(60)