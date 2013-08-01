import pymunk
from draw2d import *

class Player():
	def __init__(self, pos, space):
		self.name = "Untitled"
		self.mass = 1
		self.r = 10
		inertia = pymunk.moment_for_circle(self.mass, 0, self.r)
		self.body = pymunk.Body(self.mass, inertia)
		self.body.position = pos
		self.shape = pymunk.Circle(self.body, self.r)
		space.add(self.body, self.shape)
	
	def draw(self):
		circle(red, self.body.position, self.r)
	
	def update(self, dt):
		pass
