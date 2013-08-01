from OpenGL.GL import *
from math import *
from texture import Texture
from pygame.font import Font

black = 0,0,0,1
white = 1,1,1,1
red   = 1,0,0,1
green = 0,1,0,1
blue  = 0,0,1,1
cyan  = 0,1,1,1
magenta = 1,0,1,1
yellow = 1,1,0,1

def transparent(t, (r,g,b,a)):
	return (r,g,b,t*a)

def setCol((r,g,b,a)):
	glColor4f(r,g,b,a)

def shape(shape, points):
	glBegin(shape)
	for x, y in points:
		glVertex2f(x, y)
	glEnd()

def poly(col, points):
	setCol(col)
	shape(GL_TRIANGLE_FAN, points)

def rect(col, (x1, y1), (x2, y2)):
	setCol(col)
	shape(GL_QUADS, [(x1,y1), (x1,y2), (x2,y2), (x2,y1)])

def circle(col, (x, y), r):
	setCol(col)
	shape(GL_TRIANGLE_FAN, [(x + r*sin(a), y + r*cos(a))
				for a in map(lambda x: 2*pi*x/r,
						range(r))])

def sprite(tex, (x, y), a=1):
	setCol(transparent(a, white))
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D,tex.texID)
	glBegin(GL_QUADS)
	for dx, dy in [(0,0), (0,1), (1,1), (1,0)]:
		glTexCoord2f(dx,dy)
		glVertex2f(x+tex.w*dx, y+tex.h*dy)
	glEnd()
	glDisable(GL_TEXTURE_2D)

def text(text, font, pos, col=(255, 255, 255, 255), bg=(0,0,0,0)):
	img = font.render(text, True, col, bg)
	tex = Texture(img)
	translated(pos,
		scaled, (0, img.get_height()/2), (1, -1),
			sprite, tex, (0,0))

def font(size, file=None):
	return Font(file, size)

def texpoly(tex, (ox, oy), points, a=1):
	setCol(transparent(a, white))
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D,tex.texID)
	glBegin(GL_TRIANGLE_FAN)
	for x, y in points:
		dx, dy = 1.*(x-ox)/tex.w, 1.*(y-oy)/tex.h
		glTexCoord2f(dx,dy)
		glVertex2f(x, y)
	glEnd()
	glDisable(GL_TEXTURE_2D)

def texquads(tex, (ox, oy), pointsa, pointsb, a=1):
	setCol(transparent(a, white))
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D,tex.texID)
	glBegin(GL_QUAD_STRIP)
	points = [point
		for pair in zip(pointsa, pointsb)
		for point in pair]
	for x, y in points:
		dx, dy = 1.*(x-ox)/tex.w, 1.*(y-oy)/tex.h
		glTexCoord2f(dx,dy)
		glVertex2f(x, y)
	glEnd()
	glDisable(GL_TEXTURE_2D)


def with_transform(transform, fun, *args, **kwd):
	glPushMatrix()
	transform()
	fun(*args, **kwd)
	glPopMatrix()

def translated((x, y), fun, *args, **kwd):
	f = lambda: glTranslatef(x, y, 0)
	with_transform(f, fun, *args, **kwd)

def translate((tx, ty), (x, y)):
	return tx+x, ty+y

def rotated((x, y), a, fun, *args, **kwd):
	def f():
		glTranslatef(x, y, 0)
		glRotatef(a, 0, 0, 1)
		glTranslatef(-x, -y, 0)
	with_transform(f, fun, *args, **kwd)

def rotate((ox, oy), a, (x, y)):
	dx, dy = x-ox, y-oy
	a = a*pi/180
	dx, dy = dx*cos(a)-dy*sin(a), dx*sin(a)+dy*cos(a)
	return dx+ox, dy+oy

def scaled((x, y), (sx, sy), fun, *args, **kwd):
	def f():
		glTranslatef(x, y, 0)
		glScalef(sx, sy, 1)
		glTranslatef(-x, -y, 0)
	with_transform(f, fun, *args, **kwd)

def scale((ox, oy), (sx, sy), (x, y)):
	dx, dy = x-ox, y-oy
	return ox+sx*dx, oy+sy*dy

def skewed((x, y), (sx, sy), fun, *args, **kwd):
	def f():
		glTranslatef(x, y, 0)
		glMultMatrixf([1, sy, 0, 0,
			       sx, 1, 0, 0,
			       0,  0, 1, 0,
			       0,  0, 0, 1])
		glTranslatef(-x, -y, 0)
	with_transform(f, fun, *args, **kwd)

def drawGrass(tex, ox, dy_o, dy1, dy2, points, a=1):
	for (xa, ya), (xb, yb) in zip(points, points[1:]):
		oy = dy_o + ya
		y1 = ya + dy1
		y2 = ya + dy2
		skewy = (yb - ya) / float(xb - xa)
		skewed((xa, 42), (0, skewy),
			texpoly, tex, (ox, oy), [(xa, y1), (xb, y1), (xb, y2), (xa, y2)], a=a)
