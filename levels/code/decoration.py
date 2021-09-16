import pygame as pg

from settings import vertical_tile_number, screen_width ,tile_size

from tiles import StaticTile

from support import import_folder

from random import choice,randint


class Sky:


    def __init__(self,horizon):
        self.top = pg.image.load('graphics/decoration/sky/sky_top.png').convert()
        self.middle = pg.image.load('graphics/decoration/sky/sky_middle.png').convert()
        self.bottom = pg.image.load('graphics/decoration/sky/sky_bottom.png').convert()
        self.horizon = horizon

        # strech

        self.top = pg.transform.scale(self.top,(screen_width,448))
        self.middle = pg.transform.scale(self.middle,(screen_width,448))
        self.bottom = pg.transform.scale(self.bottom,(screen_width,448))
    def draw(self,surface):
        for row in range(vertical_tile_number):
            y = row * 448
            if row < self.horizon:
                surface.blit(self.top,(0,y))
            elif  row == self.horizon:
                surface.blit(self.middle,(0,y))

            else:
                surface.blit(self.bottom,(0,y))



class Castle:
    def __init__(self,horizon):
        self.cast = pg.image.load('graphics/decoration/town.png').convert_alpha()
        self.cast = pg.transform.scale(self.cast,(screen_width,270))  
        self.horizon = horizon
    def draw(self,surface):
        for row in range(vertical_tile_number):
            y = row * 270
            if row > self.horizon:
            
                surface.blit(self.cast,(0,200))


class Clound:
    def __init__(self,horizon,level_width,clound_number):
        clound_surf_list = import_folder('graphics/decoration/clounds/')
        min_x = -screen_width
        max_x = level_width = screen_width
        min_y = 0
        max_y = horizon
        self.clound_sprites = pg.sprite.Group()

        for clound in range(clound_number):
            clound = choice(clound_surf_list)
            x = randint (min_x,max_x)

            y = randint(min_y,max_y)    

            sprite = StaticTile (0,x,y,clound)
            self.clound_sprites.add(sprite)
    
    def draw(self,surface,shift_x,shift_y):
        self.clound_sprites.update(shift_x,shift_y)
        self.clound_sprites.draw(surface)
