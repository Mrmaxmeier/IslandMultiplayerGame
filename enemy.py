import pymunk
import pygame
import random
from pygame.locals import *
from draw2d import *

class Enemy():
	def __init__(self, pos, map):
		self.type = random.choice(["default"])
		self.mass = 1
		self.r = 15
		self.map = map
		self.space = self.map.space
		inertia = pymunk.moment_for_circle(self.mass, 0, self.r)
		self.body = pymunk.Body(self.mass, inertia)
		self.body.position = pos
		self.shape = pymunk.Circle(self.body, self.r)
		self.space.add(self.body, self.shape)
		
		self.target = random.choice(map.players)
		print
		print self.type + "-typed Enemy spawned, target: "+self.target.name+" at Position: "+str(pos[0])+", "+str(pos[1])
		print
		self.health = 100
		self.damageTaken = 0
		self.damageCaused = 0
		
	
	def draw(self):
		circle(yellow, self.body.position, self.r)
	
	def update(self, dt):
		speed = 200
		target_vx = 0
		target_vy = 0
		if self.type == "default":
			if self.target.body.position[0] < self.body.position[0]:
				target_vx -= speed
			elif self.target.body.position[0] > self.body.position[0]:
				target_vx += speed
			elif self.target.body.position[1] > self.body.position[1] and self.onGround:
				target_vy += speed
		vx = self.body.velocity.x
		self.body.velocity.x = vx + (target_vx-vx)*2*dt
	
	def destroy(self):
		self.space.remove(self.body, self.shape)
