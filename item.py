import pymunk
from draw2d import *

class Item():
	def __init__(self, type, pos, space):
		self.type = type
		
		self.tex = None
		self.space = space
		
		self.mass = 1
		self.r = 10
		inertia = pymunk.moment_for_circle(self.mass, 0, self.r)
		self.body = pymunk.Body(self.mass, inertia)
		self.body.position = pos
		self.shape = pymunk.Circle(self.body, self.r)
		self.space.add(self.body, self.shape)
	
	
	def draw(self):
		if self.tex:
			sprite(tex, self.body.position, (self.x, self.y))
		else:
			circle(blue, self.body.position, self.r)
	
	
	def onPickup(player):
		if self.type == "health":
			player.health += 20
		elif self.type == "reduceDamage":
			player.damage -= 50