from draw2d import *
from mainloop import *

class Main(StdMain):
	def __init__(self):
		self.tex = Texture("../clojure/epic-space-adventure/src/assets/images/glass.png")
	
	def draw(self):
		texpoly(self.tex, pygame.mouse.get_pos(), [(0,0), (400, 100), (600, 400), (200, 300)])
		circle(transparent(0.5, cyan), (300, 200), 200)
		sprite(self.tex, (100,200))

mainloop(((600, 400), "lol", 30), Main)
