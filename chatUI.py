from draw2d import *
from pygame.locals import *

class Message:
	def __init__(self, text, font):
		self.text = text
		self.font = font
		self.a = 1
	
	def draw(self, yb):
		dx, dy = self.font.size(self.text)
		yt = yb - dy
		text(self.text, self.font, (0, yt), (255, 0, 255), self.a)
		return yt

class Chat:
	def __init__(self, sendCallback, font, y):
		self.send = sendCallback
		self.messages = []
		self.toSend = ""
		self.font = font
		self.y = y
	
	def receive(self, message):
		self.messages.insert(0, Message(message, self.font))
	
	def draw(self):
		y = self.y - self.font.size(self.toSend)[1]
		text(self.toSend, self.font, (0, y), (128, 255, 128))
		for message in self.messages:
			y = message.draw(y)
	
	def update(self, dt):
		count = 2
		for msg in self.messages:
			msg.a -= 0.02*dt*count
			if msg.a <= 0:
				self.messages.remove(msg)
			count += 1
	
	def onKey(self, event):
		if event.key == K_RETURN:
			self.send(self.toSend)
			self.toSend = ""
		elif event.key == K_BACKSPACE:
			print "Delete"
			self.toSend = self.toSend[:-1]
		else:
			self.toSend += event.unicode
