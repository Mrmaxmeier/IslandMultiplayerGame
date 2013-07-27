import socket
import thread
import pygame
import time

from player import *


PORT = 50662


class Client():
	def __init__(self, playerName):
		self.player = Player(playerName)
		self.msgToBeSent = []	#["Msg","Msg"...]
		self.sendClock = pygame.time.Clock()
	
	def displayMsg(self, msg):
		pass
	
	def sendToServer(self, msg):
		self.msgToBeSent.append(msg)
	
	
	def connectToServer(self, host, port = PORT):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((host, port))
		thread.start_new_thread(self.handle, (sock, addr))
		while 1:
			if self.msgToBeSent:
				msg = self.msgToBeSent[0]
				sock.send(msg)
			self.clock.tick(5)