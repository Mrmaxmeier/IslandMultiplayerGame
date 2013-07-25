from draw2d import *
from mainloop import *
from genIsland import *

class Main(StdMain):
	def __init__(self):
		self.dirt = Texture("./assets/textures/dirt.png")
		self.grass = Texture("./assets/textures/grass_overlay.png")
		self.island = Island()
		self.t = 0
	
	def draw(self):
		#texpoly(self.tex, pygame.mouse.get_pos(), [(0,0), (400, 100), (600, 400), (200, 300)])
		texpoly(self.dirt, pygame.mouse.get_pos(), self.island.wholePoly)
		texpoly(self.grass, pygame.mouse.get_pos(), self.island.grassPoly)
		texquads(self.dirt, pygame.mouse.get_pos(), [(100, 100), (300, 300), (500, 200)], [(100, 300), (300, 350), (500, 500)])
		circle(transparent(0.5, cyan), (300, 200), 200)
		translated(pygame.mouse.get_pos(),
			rotated, (32,32), self.t*90,
				sprite, self.dirt, (0,0))
	
	def update(self, dt):
		self.t += dt
	
	def onKey(self, event):
		if event.key == K_UP:
			self.island.newWholePoly()

mainloop(((800, 600), "lol", 30), Main)
