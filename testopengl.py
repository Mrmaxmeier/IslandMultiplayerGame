from draw2d import *
from mainloop import *
from island import *
from player import *
from chatUI import *
import pymunk
import random
from utils import *

class Main(StdMain):
	def __init__(self):
		self.dirt = Texture("./assets/textures/dirt.png")
		self.grass = Texture("./assets/textures/grass_overlay.png")
		self.rose = Texture("./assets/textures/flower_rose.png")
		self.space = SuperSpace()
		self.space.gravity = (0, 50)
		self.island = Island((400,300), self.space)
		self.island.rotate(135)
		self.players = [Player((x, random.randrange(-500, 0)), self.space) for x in range(0, 600, 20)]
		self.t = 0
		
		def onMsg(text): print repr(text)
		self.chat = Chat(onMsg, font(50), 600)
	
	def draw(self):
		#texpoly(self.tex, pygame.mouse.get_pos(), [(0,0), (400, 100), (600, 400), (200, 300)])
		#texpoly(self.dirt, pygame.mouse.get_pos(), self.island.wholePoly)
		#texpoly(self.grass, pygame.mouse.get_pos(), self.island.grassPoly)
		#skewed((300, 300), map(lambda c: (c-300)*0.01, pygame.mouse.get_pos()),
		#	circle, transparent(0.5, cyan), (300, 300), 200)
		#line1 = [(100, 100), (200, 120), (300, 50), (400, 250), (500, 200)]
		#line2 = [(x, y+100) for x, y in line1]
		#texquads(self.dirt, pygame.mouse.get_pos(), line1, line2)
		#drawGrass(self.grass, 0, 0, -63, 0, line1)
		#translated(pygame.mouse.get_pos(),
		#	rotated, (32,32), self.t*90,
		#		sprite, self.dirt, (0,0))
		
		text("Hello, World!", font(150), (100,100))
		
		self.island.draw(self)
		[player.draw() for player in self.players]
		self.chat.draw()
	
	def update(self, dt):
		self.t += dt
		self.space.step(dt)
		if random.random() < dt*0.5:
			self.chat.receive("Bla, %d\nloollsd" % self.t)
		self.chat.update(dt)
	
	def onKey(self, event):
		if event.key == K_UP:
			self.island.newWholePoly()
		else:
			self.chat.onKey(event)

mainloop(((800, 600), "IslandGame", 30), Main)
