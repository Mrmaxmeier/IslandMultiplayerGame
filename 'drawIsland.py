import random
import turtle

class Island():
	def __init__(self):
		self.polyUpper = []
		self.polyLower = []
		
		self.middle = [0,0]
		
		self.genPoly()
		self.polyWidth = 0
		#self.rotate()
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
		
	def rotate(self, ori):
		pass
	def reCompute(self):
		pass

island1 = Island()
print(island1.polyUpper, "\nBlaah\n", island1.polyLower)




def draw(x, y):
	turtle.up()
	turtle.goto(island1.polyUpper[0][0]+x, island1.polyUpper[0][1]+y)
	turtle.down()
	
	for i in island1.polyUpper:
		turtle.goto(i[0]+x,i[1]+y)
		turtle.dot(5, "red")
	turtle.up()
	turtle.goto(island1.polyLower[0][0]+x, island1.polyLower[0][1]+y)
	turtle.down()
	for i in island1.polyLower:
		turtle.goto(i[0]+x,i[1]+y)
		turtle.dot(5, "red")



def cPoly(island):
	cpoly = island.polyUpper
	cpoly += reversed(island.polyLower)
	return cpoly

def cDraw(cpoly, x, y):
	turtle.up()
	turtle.goto(cpoly[0][0]+x,cpoly[0][1]+y)
	turtle.down()
	lastX = cpoly[-1][0]
	for i in cpoly:
		turtle.goto(i[0]+x,i[1]+y)
		turtle.dot(5, "red")
		if i[0] > lastX:
			turtle.dot(10,"green")
		
		lastX = i[0]

	turtle.goto(cpoly[0][0]+x,cpoly[0][1]+y)
	turtle.dot(5, "red")

#draw(0, 0)
#island1.genPoly()
#draw(-200, -200)
#island1.genPoly()
#draw(200, 200)
#island1.genPoly()
#draw(-400, 0)

def drawmiddle(island, x, y):
	turtle.up()
	turtle.goto(island.middle[0] +x,island.middle[1] +y)
	turtle.down()
	turtle.dot(20,"blue")

islands = []
coords = [[0,0],[300,300],[-300,-300],[-300,300],[300,-300]]

for i in range(5):
	isl = Island()
	islands.append(isl)


for isl in islands:
	x,y = coords[0]
	isl.genPoly()
	drawmiddle(isl,x,y)
	cDraw(cPoly(isl), x,y)
	
	coords.remove(coords[0])




import Tkinter
Tkinter.mainloop()