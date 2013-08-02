import socket
import thread
import pygame
import time

from commandHandler import *
from player import *

from draw2d import *
from mainloop import *
from island import *

from chatUI import *


PORT = 50662


class Client(StdMain):
	def __init__(self):
		self.map = Map()
		
		self.player = Player((0,0), self.map.space)
		self.msgToBeSent = []	#["Msg","Msg"...]
		self.sendclock = pygame.time.Clock()
		self.gameclock = pygame.time.Clock()
		self.gameState = "mainmenu"
		
		
		pygame.init()
		self.chat = Chat(self.sendToServer, font(50), 600)
		
		
		
		self.connectTo = ""
		
		self.t = 0
		
		self.cmdObj = clientCommandHandlerObj(self)
	
	
	def update(self, dt):
		self.t += dt
		if self.gameState == "ingame":
			self.ingame_update(dt)
	
	
	
	def displayMsg(self, msg):
		pass
	
	def sendToServer(self, msg):
		print "sending: "+msg
		self.msgToBeSent.append(msg)
	
	
	def connectToServer(self, host, port = PORT):
		try:
			addr = ((host, port))
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect(addr)
			thread.start_new_thread(self.chandle, (sock, addr))
			while 1:
				if self.msgToBeSent:
					msg = self.msgToBeSent[0]
					sock.send(msg)
					self.msgToBeSent.remove(msg)
				self.sendclock.tick(5)
		except Exception as e:
			print e
	
	def chandle(self, sock, addr):
		try:
			print "connected to", addr
			while 1:
				msg = sock.recv(1024)
				if msg:
					print "received "+msg
					self.chat.receive(msg)
					self.cmdObj.clientIncomingMsg(msg)
			
				else:
					self.gameState = "mainmenu"
					print addr, "closed!"
					return
		except Exception as e:
			print e
	
	
	def ingame_update(self, dt):
		

		self.map.space.step(dt)
		self.chat.update(dt)
		
		
		self.gameclock.tick(30)
		self.player.update(dt)
	
	def ingame_draw(self):
		text("INGAME 2GO", font(50), (50, 200))
		self.gameclock.tick(30)
		self.chat.draw()
	
	
	def draw(self):
		if self.gameState == "mainmenu":
			self.mainmenu_draw()
		elif self.gameState == "changeNick":
			self.changeNick_draw()
		elif self.gameState == "directConnect":
			self.directConnect_draw()
		elif self.gameState == "ingame":
			self.ingame_draw()
		
		else:
			text("NO VALID GAMESTATE", font(100), (0,0))
			text("Current Gamestate: "+self.gameState, font(50), (0,100))
	
	
	def mainmenu_draw(self):
		text("Main Menu:", font(150), (0,0))
		text("1: Bonjour", font(75), (50, 100))
		text("2: Direct Connect", font(75), (50, 150))
		text("3: Change Nick", font(75), (50, 200))

		text("Current Nick: "+self.player.name, font(75), (50, 300))
	
	def changeNick_draw(self):
		if self.player.name == "":
			text("Type to change Nick", font(50), (50, 200))
		else:
			text("Press <ENTER> to finish your Name.", font(50), (50, 200))
		text("Current Nick: "+self.player.name, font(75), (50, 300))
	
	def directConnect_draw(self):
		if self.player.name == "":
			text("Type in the IP/Hostname.", font(50), (50, 200))
		else:
			text("Press <ENTER> to finish.", font(50), (50, 200))
		text("Current IP: "+self.connectTo, font(75), (50, 300))
		
	
	
	def onKey(self, event):
		if self.gameState == "mainmenu":
			if event.key == K_3:
				self.player.name = ""
				self.gameState = "changeNick"
			if event.key == K_2:
				self.gameState = "directConnect"
			if event.key == K_1:
				self.gameState = "bonjourScan"
		elif self.gameState == "changeNick":
			if event.key == K_RETURN:
				self.gameState = "mainmenu"
			elif event.key == K_BACKSPACE:
				self.player.name = self.player.name[:-1]
			else:
				self.player.name += event.unicode
		elif self.gameState == "directConnect":
			if event.key == K_RETURN:
				thread.start_new_thread(self.connectToServer, (self.connectTo,))
				
				self.gameState = "ingame"
			elif event.key == K_BACKSPACE:
				self.connectTo = self.connectTo[:-1]
			else:
				self.connectTo += event.unicode
		elif self.gameState == "ingame":
			if False:
				pass
			else:
				self.chat.onKey(event)






if __name__ == "__main__":
	#host = raw_input("Connect To Host: ")
	#playerName = raw_input("Your Name: ")
	client = Client()
	mainloop(((800, 600), "FlyLands", 30), Client)
	#thread.start_new_thread(client.connectToServer, (host,))
	
	#client.mainloop()
