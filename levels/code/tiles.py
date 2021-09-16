import pygame as pg
from support import import_folder

class Tile (pg.sprite.Sprite):
    def __init__ (self,size,x,y):
        super().__init__()
        self.image =  pg.Surface((size,size))
        
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self,shift_x,shift_y):
        self.rect.x +=shift_x
        self.rect.y +=shift_y


class StaticTile(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__ (size,x,y)
        self.image = surface



class Grass (StaticTile):
    def __init__ (self,size,x,y):
        super(). __init__ (size,x,y,pg.image.load('./gothicvania patreon collection/decoration/gras1_32px.png').convert_alpha())
        offset_y =  y +size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))


class Rock (StaticTile):
    def __init__ (self,size,x,y):
        super(). __init__ (size,x,y,pg.image.load('./gothicvania patreon collection/decoration/rockpile_128px.png').convert_alpha())
        offset_y =  y +size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))


class Tree (StaticTile):
    def __init__ (self,size,x,y):
        super(). __init__ (size,x,y,pg.image.load('./gothicvania patreon collection/decoration/tree_64px.png').convert_alpha())
        offset_y =  y +size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))


class AnimatedTile(Tile):
    def __init__(self,size,x,y,path):
        super(). __init__(size,x,y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
            
    def update(self,shift_x,shift_y):
        self.animate()
        self.rect.x += shift_x 
        self.rect.y += shift_y

