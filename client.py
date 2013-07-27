import socket
import thread
import pygame
import time

from commandHandler import *
from player import *


PORT = 50662


class Client():
	def __init__(self, playerName):
		self.cmdObj = clientCommandHandlerObj(self)
		
		self.player = Player(playerName)
		self.msgToBeSent = []	#["Msg","Msg"...]
		self.sendclock = pygame.time.Clock()
		self.gameclock = pygame.time.Clock()
	
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
				self.sendclock.tick(5)
		except Exception as e:
			print e
	
	def chandle(self, sock, addr):
		print "connected to", addr
		while 1:
			msg = sock.recv(1024)
			if msg:
				self.cmdObj.clientIncomingMsg(msg)
			
			else:
				print addr, "closed!"
				return
	
	
	def mainloop(self):
		self.gameclock.tick(30)






if __name__ == "__main__":
	host = raw_input("Connect To Host: ")
	playerName = raw_input("Your Name: ")
	client = Client(playerName)
	thread.start_new_thread(client.connectToServer, (host,))
	
	client.mainloop()