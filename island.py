from draw2d import *

import random
import pymunk
import time

from item import *


class Map():
	def __init__(self, clientside, seed = None):
		self.clientside = clientside
		if seed:
			self.seed = seed
		else:
			self.seed = time.time()
		self.islands = []
		self.islseed2isl = {} #{Seed:Island, }
		
		self.players = []
		self.name2player = {} #{Name:Player}


		
		self.items = []
		

		self.space = pymunk.Space()
		self.space.gravity = (0, 50)
		
		if self.clientside:
			self.dirt = Texture("./assets/textures/dirt.png")
			self.grass = Texture("./assets/textures/grass_overlay.png")
			self.rose = Texture("./assets/textures/flower_rose.png")
			self.dandelion = Texture("./assets/textures/flower_dandelion.png")
			self.carrots = Texture("./assets/textures/carrots_stage.png")
			self.sapling_birch = Texture("./assets/textures/sapling_birch.png")
			self.sapling_oak = Texture("./assets/textures/sapling_oak.png")

	
	def genIslands(self):
		for num in range(10):
			random.seed(self.seed + num)
			pos = (random.randrange(50, 100)+num*500, random.randrange(50,500))
			isl = Island(pos, self.space)
			isl.seed = self.seed + num
			self.islseed2isl[isl.seed] = isl
			self.islands.append(isl)
		print
		print "Generated "+str(len(self.islands))+" Islands in total."
		print
	
	def draw(self):
		for island in self.islands:
			island.draw(self)
		for player in self.players:
			player.draw()
		for item in self.items:
			item.draw()
	
	
	
	def update(self, dt):
		for island in self.islands:
			for plant in island.plants:
				plant.update(dt, self)
	


class Plant:
	def __init__(self, island):
		mx, my = island.middle
		self.island = island
		self.x = random.randrange(mx*2)
		for (x1, y1), (x2, y2) in zip(island.polyUpper, island.polyUpper[1:]):
			if x2 > self.x:
				dx1, dx2 = self.x-x1, x2-x1
				dy = y2-y1
				self.slope = dy/float(dx2)
				self.y = y1 + dy*float(dx1)/dx2
				break
		
		self.texInt = random.randrange(1, 6)
		
	def draw(self, map):
		tex = self.getTex(map)
		midx, boty = tex.w/2, tex.h
		skewed((self.x, self.y), (0, self.slope), scaled, (self.x, self.y), (1, -1), sprite, tex, (self.x-midx, self.y))
	
	def getTex(self, map):
		if self.texInt == 2:
			return map.dandelion
		elif self.texInt == 3:
			return map.sapling_oak
		elif self.texInt == 4:
			return map.sapling_birch
		elif self.texInt == 5:
			return map.carrots
		else:
			return map.rose
	
	def getPos(self, (dx, dy)):
		return translate(self.island.getTranslation(), rotate(self.island.middle, self.island.body.angle*180/pi, (self.x+dx, self.y+dy)))
	
	def update(self, dt, map):
		if random.random() < dt / 10:
			if self.texInt in [4, 5]:
				itemType = random.choice(["health", "reduceDamage"])
				itemPos = self.getPos((random.randint(-100, 100), -200))
				newItem = Item(itemType, itemPos, map.space)
				map.items.append(newItem)
	

class Island():
	def __init__(self, pos, space):
		self.static_body = pymunk.Body()
		self.body = pymunk.Body(10000, 10000)
		space.add(self.body)
		self.body.position = pos
		self.newWholePoly()
		self.shapes = self.getShapes()
		space.add(self.shapes)
		self.space = space
		self.plants = self.genPlants()
		x, y = pos
		joint = pymunk.PivotJoint(self.static_body, self.body, (x, y-0))
		space.add(joint)
	
	def clearData(self):
		self.polyUpper = []
		self.polyLower = []
		self.body.angle = 0 #Nicht-Grad!
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
		px, py = self.body.position
		return px-mx, py-my
	
	def getPoly(self):
		points = self.polyUpper + list(reversed(self.polyLower))
		f = lambda p: translate(self.getTranslation(), rotate(self.middle, self.body.angle, p))
		return map(f, points)
	
	def getShapes(self):
		px, py = self.body.position
		points = [(x-px, y-py) for x, y in self.getPoly()]
		tris = pymunk.util.triangulate(points)
		self.tris = tris
		return [pymunk.Poly(self.body, tri) for tri in tris]
	
	def newWholePoly(self):
		self.clearData()
		self.genPoly()
	
	def genEyeCandy(self):
		objNum = self.polyWidth/4
	
	def rotate(self, drot):
		self.body.angle += drot*pi/180
	
	def draw(self, main):
		def draw():
			for plant in self.plants:
				plant.draw(main)
			texquads(main.dirt, self.middle, self.polyUpper, self.polyLower)
			drawGrass(main.grass, 0, 0, -63, 0, self.polyUpper)
		translated(self.getTranslation(), rotated, self.middle, self.body.angle*180/pi, draw)
	
	def genPlants(self):
		return [Plant(self) for i in range(5)]

