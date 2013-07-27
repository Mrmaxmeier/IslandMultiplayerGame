import random
from draw2d import *

class Island():
	def __init__(self, pos):
		self.pos = pos
		self.newWholePoly()
	
	def clearData(self):
		self.polyUpper = []
		self.polyLower = []
		self.rot = 0 #Grad
		self.middle = (0,0)
		self.polyWidth = 0
		self.grassLine = []
		self.eyeCandy = []
		self.trees    = []
	
	def genPoly(self):
		self.polyUpper = []
		self.polyLower = []
		self.polyWidth = random.randrange(15, 30)
		
		self.middle = [ 10 * self.polyWidth, self.polyWidth/2 ** 2,]
		
		self.curx = 0
		
		for i in range(self.polyWidth):
			ymod = abs(i - self.polyWidth/2)
			ymod = self.polyWidth/2 - ymod
			ymod = ymod  * 4
			#print(i, ymod)
			self.curx += 20
			self.polyUpper.append([self.curx, random.randrange(5, 10) - ymod])
		
		self.curx = 0
		for i in range(self.polyWidth):
			ymod =  abs(i - self.polyWidth/2)
			ymod =  self.polyWidth/2 - ymod
			ymod =  ymod ** 2 * 2
			ymod += -self.polyWidth * 1#4.9
			self.curx += random.randrange(15, 20)
			self.polyLower.append([self.curx, random.randrange(25, 50) + ymod])
	
	def getPoly(self):
		points = self.polyUpper
		points += reversed(self.polyLower)
		f = lambda p: translate(self.pos, rotate(self.middle, self.rot, p))
		return map(trafo, points)
	
	def newWholePoly(self):
		self.clearData()
		self.genPoly()
	
	def genEyeCandy(self):
		objNum = self.polyWidth/4
	
	def rotate(self, drot):
		self.rot += drot
	
	def draw(self, main):
		def draw():
			texquads(main.dirt, self.middle, self.polyUpper, self.polyLower)
			drawGrass(main.grass, 0, 0, -63, 0, self.polyUpper)
		translated(self.pos, rotated, self.middle, self.rot, draw)

