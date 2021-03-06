import pygame 
from tiles import AnimatedTile
from random import randint

class Enemy (AnimatedTile):
	def __init__(self,size,x,y):
		super().__init__(size,x,y,'C:/Users/Lucas Angulski/Desktop/lucas pygame project/graphics/enemy/idle')
		self.rect.y += size - self.image.get_size()[1]
		self.speed = randint(1,3)

	def move(self):
		self.rect.x += self.speed

	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image,True,False)

	def reverse(self):
		self.speed *= -1

	def update(self,shift_x,shift_y):
		self.rect.x += shift_x
		self.rect.y += shift_y
		self.move()
		self.animate()
		self.reverse_image()