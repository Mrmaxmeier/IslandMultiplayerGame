from draw2d import *
from mainloop import *
from genIsland import *

class Main(StdMain):
	def __init__(self):
		self.dirt = Texture("./assets/textures/dirt.png")
		self.grass = Texture("./assets/textures/grass_overlay.png")
		self.island = Island()
	
	def draw(self):
		#texpoly(self.tex, pygame.mouse.get_pos(), [(0,0), (400, 100), (600, 400), (200, 300)])
		texpoly(self.dirt, pygame.mouse.get_pos(), self.island.wholePoly)
		texpoly(self.grass, pygame.mouse.get_pos(), self.island.grassPoly)
		circle(transparent(0.5, cyan), (300, 200), 200)
		sprite(self.dirt, (100,200))
	def update(self, dt):
		for event in pygame.event.get():
			if event.type == QUIT:
				print "QUIT"
			elif event.type == KEYDOWN:
				if event.key == K_UP:
					self.island.newWholePoly()

mainloop(((800, 600), "lol", 30), Main)
