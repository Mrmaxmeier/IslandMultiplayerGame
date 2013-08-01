import random
from draw2d import *
import pymunk

class Island():
	def __init__(self, pos, space):
		self.body = pymunk.Body()
		self.pos = pos
		self.newWholePoly()
		self.shapes = self.getShapes()
		space.add(self.shapes)
		self.space = space
	
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
	
	def getTranslation(self):
		mx, my = self.middle
		px, py = self.pos
		return px-mx, py-my
	
	def getPoly(self):
		points = self.polyUpper + list(reversed(self.polyLower))
		f = lambda p: translate(self.getTranslation(), rotate(self.middle, self.rot, p))
		return map(f, points)
	
	def getShapes(self):
		mx, my = self.middle
		points = self.getPoly()
		tris = pymunk.util.triangulate(points)
		self.tris = tris
		return [pymunk.Poly(self.body, tri) for tri in tris]
	
	def newWholePoly(self):
		self.clearData()
		self.genPoly()
	
	def genEyeCandy(self):
		objNum = self.polyWidth/4
	
	def rotate(self, drot):
		self.rot += drot
		self.space.remove(self.shapes)
		self.shapes = self.getShapes()
		self.space.add(self.shapes)
	
	def draw(self, main):
		def draw():
			texquads(main.dirt, self.middle, self.polyUpper, self.polyLower)
			drawGrass(main.grass, 0, 0, -63, 0, self.polyUpper)
		translated(self.getTranslation(), rotated, self.middle, self.rot, draw)

