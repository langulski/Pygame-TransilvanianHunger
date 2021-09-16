import pygame as pg
from support import import_folder


class Player (pg.sprite.Sprite):
    def __init__(self,pos,surface,create_jump_particles):
        super().__init__()
        self.frame_index =0

        self.animation_speed = 0.10

        self.import_character_assets()
        self.image = self.animations['idle'][self.frame_index]
      
        self.rect = self.image.get_rect(topleft=pos)
        
        #player movment
        self.speed = 6
        self.direction = pg.math.Vector2(0,0)
        self.gravity = 0.8
        self.jump_speed = -16
        self.collision_rect = pg.Rect(self.rect.topleft,(30,self.rect.height))


        #player attack
        # self.create_attack_particles = create_attack_particles
        self.import_attack_particles()
        self.attack_frame_index = 0
        self.attack_animation_speed = 0.05
        self.attack1 = False
        #dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.12
        self.display_surface = surface
        self.create_jump_particles =  create_jump_particles

        #plyaer status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    

    def import_character_assets(self):
        character_path = 'graphics/character/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'attack':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def import_dust_run_particles(self):
        
        self.dust_run_particles = import_folder('./graphics/character/dust_particles/run')   
    
    def import_attack_particles(self):
        
        self.attack_particles = import_folder('./graphics/character/dust_particles/attack')   
        

    def animate(self):
        animation = self.animations[self.status]

        #loop frame
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
       
        image=animation[int(self.frame_index)]
        if self.facing_right:
            self.image=image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pg.transform.flip(image,True,False)
            self.image=flipped_image
            self.rect.bottomright = self.collision_rect.bottomright
        # set the rect 
        # if self.on_ground and self.on_right:
        #      self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        # elif self.on_ground and self.on_left:
        #      self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        # elif self.on_ceiling and self.on_right:
        #      self.rect = self.image.get_rect(topright = self.rect.topright)
        # elif self.on_ceiling and self.on_left:
        #      self.rect = self.image.get_rect(topleft = self.rect.topleft)
        # elif self.on_ceiling:
        #      self.rect = self.image.get_rect(midtop = self.rect.midtop)
        # elif self.on_ground:
        #      self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        # elif self.on_ground and on_ceiling :
        #      self.rect = self.image.get_rect(bottom = self.rect.bottom)
    
       
    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]
            if self.facing_right:
                 pos = self.rect.bottomleft - pg.math.Vector2(6,10)
                 self.display_surface.blit(dust_particle,pos)
            
            else:
                 pos = self.rect.bottomright - pg.math.Vector2(6,10)
                 flipped_dust_particle = pg.transform.flip(dust_particle,True,False)
                 self.display_surface.blit(flipped_dust_particle,pos)
    







    def get_input(self):

        keys = pg.key.get_pressed()

        if keys[pg.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pg.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pg.K_UP] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)
    
        elif keys[pg.K_SPACE]:
            self.attack1 = True
            self.run_attack_animation()
            

        else:
            self.direction.x = 0
        
    def run_attack_animation(self):
        if self.attack1 == True:
            self.attack_frame_index += self.attack_animation_speed
            if self.attack_frame_index >= len(self.attack_particles):
                self.attack_frame_index = 0
        
            attack_particle = self.attack_particles[int(self.attack_frame_index)]
            attack_particle.set_colorkey((0, 0, 0))
            if self.facing_right:
                 pos = self.rect.bottomleft - pg.math.Vector2(-15,45)
                 self.display_surface.blit(attack_particle,pos)
            
            else:
                 pos = self.rect.bottomright - pg.math.Vector2(75,45)
                 flipped_attack_particle = pg.transform.flip(attack_particle,True,False).convert()
                 flipped_attack_particle.set_colorkey((0, 0, 0))
                 self.display_surface.blit(flipped_attack_particle,pos)
        


    def get_status(self):
        if self.direction.y <0:
            self.status = 'jump'
        elif self.direction.y >1:
            self.status = 'fall'
        else:
            if self.direction.x !=0:
                self.status = 'run'

            elif self.attack1 == True:
                self.status = 'attack'
                self.attack1=False
            else:
                self.status = 'idle'
        # print(self.status)
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.direction.y =self.jump_speed

    



    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
      
        pg.draw.rect(self.display_surface,'red',self.collision_rect)
        