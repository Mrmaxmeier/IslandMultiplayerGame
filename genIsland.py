import random

class Island():
	def __init__(self):
		self.polyUpper = []
		self.polyLower = []
		
		self.middle = [0,0]
		
		self.genPoly()
		self.polyWidth = 0
		#self.rotate()
		
		self.wholePoly = []
		self.newWholePoly()
		
	def genPoly(self):
		self.polyUpper = []
		self.polyLower = []
		self.polyWidth = random.randrange(15, 30)
		
		self.middle = [ 10 * self.polyWidth, self.polyWidth/2 ** 2,]
		
		self.curx = 0
		
		#print(self.polyWidth)
		
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
	
	
	def cPoly(self):
		cpoly = self.polyUpper
		cpoly += reversed(self.polyLower)
		return cpoly
	
	def newWholePoly(self):
		self.genPoly()
		self.wholePoly = self.cPoly()
		
	def rotate(self, ori):
		pass
	def reCompute(self):
		pass

