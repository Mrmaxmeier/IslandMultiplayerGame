import pymunk
from draw2d import *

class Item():
	def __init__(self, type, pos, space):
		self.type = type
		
		self.tex =  Texture("./assets/textures/apple.png")#None
		self.space = space
		
		self.mass = 1
		self.scale = 0.75
		self.r = 32*self.scale
		inertia = pymunk.moment_for_circle(self.mass, 0, self.r)
		self.body = pymunk.Body(self.mass, inertia)
		self.body.position = pos
		self.shape = pymunk.Circle(self.body, self.r)
		self.space.add(self.body, self.shape)
	
	
	def draw(self):
		if self.tex:
			w, h = self.tex.w, self.tex.h
			scaled(self.body.position, (self.scale, -self.scale), sprite, self.tex, translate((w/-2., h/-2.), self.body.position))
		else:
			circle(blue, self.body.position, self.r)
	
	
	def onPickup(player):
		if self.type == "health":
			player.health += 20
		elif self.type == "reduceDamage":
			player.damage -= 50
