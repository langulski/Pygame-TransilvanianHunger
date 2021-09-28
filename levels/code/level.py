import pygame as pg
from support import import_csv_layout, import_cut_graphics
from settings import tile_size,screen_height,screen_width
from tiles import Tile, StaticTile, Grass, Rock, Tree
from enemy import Enemy
from decoration import Sky, Castle , Clound
from particles import ParticleEffect
from player import Player


class Level:
    def __init__ (self,level_data,surface):
        
        #general
        self.display_surface = surface
        self.world_shift = 0
        self.world_shift_y = 0
        self.current_x = None
        #player_layout
        player_layout = import_csv_layout(level_data['player'])
        self.player = pg.sprite.GroupSingle()
        self.goal = pg.sprite.GroupSingle()
        self.player_setup(player_layout)

        #dust 
        self.dust_sprite = pg.sprite.GroupSingle()
        self.player_on_ground = False


        #terrain
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

        #grass
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout,'grass')
        
        #rock 
        rock_layout = import_csv_layout(level_data['rock'])
        self.rock_sprites = self.create_tile_group(rock_layout,'rock')

        #background
        background_layout = import_csv_layout(level_data['background'])
        self.background_sprites = self.create_tile_group(background_layout,'background')


        #tree 

        tree_layout = import_csv_layout(level_data['tree'])
        self.tree_sprites = self.create_tile_group(tree_layout, 'tree')

        #enemy 
        enemy_layout = import_csv_layout(level_data['enemy'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemy')


        # hitbox for the enemies
        constraint_layout = import_csv_layout(level_data['hitbox'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'hitbox')


        #decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0])*tile_size
        self.castle = Castle(9)
        self.clounds = Clound(900,level_width,80)


    def create_tile_group(self,layout,type):
        sprite_group = pg.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                   
                    x = col_index * tile_size
                   
                    y =  row_index * tile_size
                    
                    if type =='terrain':
                        terrain_tile_list = import_cut_graphics('./gothicvania patreon collection/Old-dark-Castle-tileset-Files/PNG/old-dark-castle-interior-tileset1.png')
                        tile_surface = terrain_tile_list[int(val)]
                        # print(tile_surface)
                        sprite = StaticTile(tile_size,x,y,tile_surface)

                    if type =='background':
                        background_tile_list = import_cut_graphics('./gothicvania patreon collection/Old-dark-Castle-tileset-Files/PNG/old-dark-castle-interior-tileset1.png')
                        tile_surface = background_tile_list[int(val)]
                        # print(tile_surface)
                
                        sprite = StaticTile(tile_size,x,14+y,tile_surface)
                    
                    if type =='grass':
                        
                        sprite = Grass(tile_size,x,y)
                        
                    if type == 'rock':
                        sprite = Rock(tile_size,x,y)
                    

                    if type == 'tree':
                        sprite = Tree(tile_size,x,y)

                    if type == 'enemy':
                        sprite = Enemy(tile_size,x,y)
                    
                    if type =='hitbox':
                        sprite = Tile(50,x,y-26)

                    
                    
                    
                    
                    
                    
                
                    
                    sprite_group.add(sprite)
        
        return sprite_group

    def player_setup(self,layout):
       for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y =  row_index * tile_size 
                if val == '0':
                    sprite = Player((x,y),self.display_surface,self.create_jump_particles)
                    self.player.add(sprite)

                if val == '1' :
                    bonfire = pg.image.load('graphics/character/bonfire_frm1_64.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,bonfire)
                    self.goal.add(sprite)


    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pg.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse()

    def create_jump_particles(self,pos):
        if self.player.sprite.facing_right:
            pos -= pg.math.Vector2(10,5)
        else:
            pos += pg.math.Vector2(10,-5)
        jump_particles_sprite = ParticleEffect(pos,'jump')
        self.dust_sprite.add(jump_particles_sprite)

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset= pg.math.Vector2(7,5)
            else:
                offset= pg.math.Vector2(-7,5)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom,'land')
            self.dust_sprite.add(fall_dust_particle)

    def horizontal_movement_collision(self):
        player = self.player.sprite

        player.collision_rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x <0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right=sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right 
            
        # if player.on_left and (player.rect.left < self.current_x or player.direction.x >=0):
        #      player.on_left= False
        # if player.on_right and (player.rect.right > self.current_x or player.direction.x <=0):
        #      player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        
        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y= 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top=sprite.rect.bottom
                    player.direction.y=0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
            
            # if player.on_ground and player.direction.y <0 or player.direction.y > 1:
            #     player.on_ground = False
            # if player.on_ceiling and player.direction.y > 0 :
            #     player.on_ceiling = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 6
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -6
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 6
    
    def scroll_y(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        player_y = player.rect.centery
        direction_y = player.direction.y
        direction_x = player.direction.x

        if player_y < screen_height / 2 and direction_y < 0:
            self.world_shift_y = 8
            if player_x < screen_width / 4 and direction_x < 0:
                self.world_shift = 6
                player.speed = 0
            elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
                self.world_shift = -6
                player.speed = 0
            
        elif player_y > screen_height - (screen_height / 4) and direction_y > 0:
            self.world_shift_y = -16
            if player_x < screen_width / 4 and direction_x < 0:
                self.world_shift = 6
                player.speed = 0
            elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
                self.world_shift = -6
                player.speed = 0
            
            
        else:
            self.world_shift_y = 0  


    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False
    
    
    def run(self):
       #world shift
        self.scroll_x()
        self.scroll_y()
        #decoration

            #sky
        self.sky.draw(self.display_surface)
        self.clounds.draw(self.display_surface,self.world_shift,self.world_shift_y) 
        #castle
        self.castle.draw(self.display_surface) 

        # grass
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift,self.world_shift_y)
        
        #rock
        self.rock_sprites.draw(self.display_surface)
        self.rock_sprites.update(self.world_shift,self.world_shift_y)
        
        #tree
        self.tree_sprites.draw(self.display_surface)
        self.tree_sprites.update(self.world_shift,self.world_shift_y)

       
        
        #background
        self.background_sprites.draw(self.display_surface)
        self.background_sprites.update(self.world_shift,self.world_shift_y)


        # enemy
        self.enemy_sprites.update(self.world_shift,self.world_shift_y)
        self.constraint_sprites.update(self.world_shift,self.world_shift_y)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)


        #dust
        self.dust_sprite.update(self.world_shift,self.world_shift_y)
        self.dust_sprite.draw(self.display_surface)

        #player sprites
        self.player.update()
        self.goal.draw(self.display_surface)
        self.goal.update(self.world_shift,self.world_shift_y)
        self.get_player_on_ground()
        self.player.draw(self.display_surface)
        self.create_landing_dust()
        
        #running the level
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift,self.world_shift_y)
        #collision player
        self.vertical_movement_collision()
        self.horizontal_movement_collision()
