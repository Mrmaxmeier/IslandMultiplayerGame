import socket
import thread
import pygame
from supersocket import SuperSocket

print "Imported Pygame, initing..."
pygame.init()
print "inited."

import time
import ConfigParser
Config = ConfigParser.ConfigParser()

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

try:
	Config.read("./settings.ini")
	Name = ConfigSectionMap("Client")['name']
	IP = ConfigSectionMap("Client")['ip']
except Exception as e:
	print e
	print "No Configfile avalible."
	print "Creating one..."
	cfgfile = open("./settings.ini",'w')
	try:
		Config.add_section('Client')
		Config.add_section('servers')
	except:
		print "Corrupted file."
	Config.set('Client','name',"")
	Name = ""
	Config.set('Client','ip', "")
	IP = ""
	Config.write(cfgfile)
	cfgfile.close()

from commandHandler import *
from player import *

from draw2d import *
from mainloop import *
from island import *

from chatUI import *





PORT = 50662


class Client(StdMain):
	def __init__(self):
		self.map = Map(True)
		
		self.name = Name
		
		self.msgToBeSent = []	#["Msg","Msg"...]
		self.sendclock = pygame.time.Clock()
		self.gameclock = pygame.time.Clock()
		self.gameState = "mainmenu"
		
		self.chat = Chat(self.send, font(50), 600)
		
		
		
		self.connectTo = IP
		
		self.t = 0
		
		self.cmdObj = clientCommandHandlerObj(self)
	
	
	def update(self, dt):
		self.t += dt
		if self.gameState == "mainmenu":
			self.chat.update(dt)
		if self.gameState == "ingame":
			self.ingame_update(dt)
	
	
	
	
	def send(self, msg):
		if self.gameState == "servers":
			if ":" in msg:
				name, ip = msg.split(":")
				cfgfile = open("./settings.ini",'w')
				Config.set('servers',name,ip)
				Config.write(cfgfile)
				cfgfile.close()
			else:
				name = msg
				ip = ConfigSectionMap("servers")[name]
			thread.start_new_thread(self.connectToServer, (ip,))
			self.gameState = "ingame"
		else:
			self.sendToServer(msg)
	
	def sendToServer(self, msg):
		print "sending: "+msg
		self.msgToBeSent.append(msg)
	
	
	def connectToServer(self, host, port = PORT):
		try:
			addr = ((host, port))
			print "Trying to connect to", addr
			sock_raw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock_raw.connect(addr)
			sock = SuperSocket(sock_raw)
			sock.send(self.name)
			thread.start_new_thread(self.chandle, (sock, addr))
			while 1:
				for msg in self.msgToBeSent:
					sock.send(msg)
				self.msgToBeSent = []
				
				if self.map.name2player.has_key(self.name):
					player = self.map.name2player[self.name]
					x, y = player.body.position
					vx, vy = player.body.velocity
					self.sendToServer("!playerPosition %f %f %f %f" % (x, y, vx, vy))
					if y > 600:
						player.body.position = (random.randrange(0, 800), 0)
						player.body.velocity = (0,0)
						self.sendToServer("!death void")
				else:
					print "waiting for response!"
				
				self.sendclock.tick(5)
		except Exception as e:
			print e
			self.chat.receive("Error connecting to Server!")
			self.gameState = "mainmenu"
	
	def chandle(self, sock, addr):
		try:
			print "connected to", addr
			while 1:
				msg = sock.recv(1024)
				if msg != None:
					print "received "+msg
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
		
		self.map.update(dt)
		
		self.gameclock.tick(30)
	
	def ingame_draw(self):
		text("INGAME 2GO", font(50), (50, 200))
		self.gameclock.tick(30)
		
		self.map.draw()
		
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
		elif self.gameState == "servers":
			self.servers_draw()
		else:
			text("NO VALID GAMESTATE", font(100), (0,0))
			text("Current Gamestate: "+self.gameState, font(50), (0,100))
	
	
	def mainmenu_draw(self):
		text("Main Menu:", font(150), (0,0))
		text("1: Bonjour", font(75), (50, 100))
		text("2: Direct Connect", font(75), (50, 150))
		text("3: Change Nick", font(75), (50, 200))
		text("4: Connect to server", font(75), (50, 250))

		text("Current Nick: "+self.name, font(75), (50, 400))
		self.chat.draw()
	
	def changeNick_draw(self):
		if self.name == "":
			text("Type to change Nick", font(50), (50, 200))
		else:
			text("Press <ENTER> to finish your Name.", font(50), (50, 200))
		text("Current Nick: "+self.name, font(75), (50, 300))
	
	def directConnect_draw(self):
		if self.name == "":
			text("Type in the IP/Hostname.", font(50), (50, 200))
		else:
			text("Press <ENTER> to finish.", font(50), (50, 200))
		text("Current IP: "+self.connectTo, font(75), (50, 300))
		
	
	def servers_draw(self):
		y = 100
		xa = 100
		xb = 300
		for name, ip in self.servers:
			text(name, font(50), (xa, y))
			text(ip, font(50), (xb, y))
			y += 50
		self.chat.draw()
	
	
	def onKey(self, event):
		if self.gameState == "mainmenu":
			if event.key == K_4:
				self.gameState = "servers"
				self.servers = ConfigSectionMap("servers").items()
			if event.key == K_3:
				self.gameState = "changeNick"
			if event.key == K_2:
				self.gameState = "directConnect"
			if event.key == K_1:
				self.gameState = "bonjourScan"
		elif self.gameState == "changeNick":
			if event.key == K_RETURN:
				cfgfile = open("./settings.ini",'w')
				Config.set('Client','name',self.name)
				Config.write(cfgfile)
				cfgfile.close()
				self.gameState = "mainmenu"
			elif event.key == K_BACKSPACE:
				self.name = self.name[:-1]
			else:
				self.name += event.unicode
		elif self.gameState == "directConnect":
			if event.key == K_RETURN:
				cfgfile = open("./settings.ini",'w')
				Config.set('Client','ip',self.connectTo)
				Config.write(cfgfile)
				cfgfile.close()
				thread.start_new_thread(self.connectToServer, (self.connectTo,))
				
				self.gameState = "ingame"
			elif event.key == K_BACKSPACE:
				self.connectTo = self.connectTo[:-1]
			else:
				self.connectTo += event.unicode
		elif self.gameState == "ingame" or self.gameState == "servers":
			self.chat.onKey(event)






if __name__ == "__main__":
	#host = raw_input("Connect To Host: ")
	#playerName = raw_input("Your Name: ")
	mainloop(((800, 600), "FlyLands", 30), Client)
	#thread.start_new_thread(client.connectToServer, (host,))
	
	#client.mainloop()
