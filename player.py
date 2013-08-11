import pymunk
import pygame
from pygame.locals import *
from draw2d import *

class Player():
	def __init__(self, pos, space):
		self.name = "Untitled"
		self.mass = 1
		self.r = 17
		inertia = pymunk.moment_for_circle(self.mass, 0, self.r)
		self.body = pymunk.Body(self.mass, inertia)
		self.body.position = pos
		self.shape = pymunk.Circle(self.body, self.r)
		space.add(self.body, self.shape)
		
		
		self.health = 100
		self.damageTaken = 0
		self.damageCaused = 0
		
	
	def draw(self):
		circle(red, self.body.position, self.r)
	
	def update(self, dt, clientname):
		speed = 200
		target_vx = 0
		if self.name == clientname:
			keys = pygame.key.get_pressed()
			if keys[K_LEFT]:
				target_vx -= speed
			if keys[K_RIGHT]:
				target_vx += speed
		vx = self.body.velocity.x
		self.body.velocity.x = vx + (target_vx-vx)*2*dt
