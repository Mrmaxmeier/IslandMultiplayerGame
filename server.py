import socket
import thread
import pygame
import time

from commandHandler import *
from player import *
from island import *

PORT = 50662


class Server():
	def __init__(self):
		self.players = []	#[PlayerObj, PlayerObj...]
		self.map = Map(time.time())
		self.chatLog = []	#[["Sender","Message","Timestamp"]]
		self.unprocessedChat= []#[["Sender","Message","Timestamp"]]
		self.cmdObj = serverCommandHandlerObj(self)
		self.sock2name = {}	#{"Sock":"Name"}
		self.name2sock = {}	#{"Name":"Sock"}
		self.socketList = []
		
		self.clock = pygame.time.Clock()
		self.gameclock = pygame.time.Clock()
		
		self.running = True
	
	
	
	
	
	def tick(self):
		if self.unprocessedChat:
			for sender, cmd, timestamp in self.unprocessedChat:
				self.cmdObj.serverIncomingMsg(cmd, sender)
				self.chatLog.append([sender, cmd, timestamp])
				print str(timestamp)+": "+sender+" -> "+cmd
				self.unprocessedChat.remove([sender, cmd, timestamp])
	
	
	def mainloop(self):
		thread.start_new_thread(self.gamemainloop, ())
		while self.running:
			self.clock.tick(5)
			self.tick()
	def gamemainloop(self):
		self.map.genIslands()
		while self.running:
			self.gameclock.tick(30)
	
	
	def newPlayer(self, player):
		self.sendToPlayer("!serverInformation mapSeed "+str(self.map.seed))
		for player in self.map.player:
			angle = player.body.angle
			pos = player.body.position
			self.sendToPlayer("!serverInformation playerPosition "+str(pos[0])+" "+str(pos[1])+" "+str(angel))
	
	
	
	
	def shandle(self, sock, addr):
		print "connected to", addr
		name = sock.recv(1024)
		self.sock2name[sock] = name
		self.name2sock[name] = sock
		self.unprocessedChat.append([name, "!join", time.time()])
		print name+" = "+addr[0]
		while 1:
			msg = sock.recv(1024*16)
			if msg:
				self.unprocessedChat.append([name, msg, time.time()])
				print addr, ":", msg
			else:
				self.unprocessedChat.append([name, "!leave", time.time()])
				print addr, "/ '" + name + "' closed!"
				self.socketList.remove(sock)
				return

	def serve(self, port, message):
		try:
			serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print (socket.gethostname(), port)
			serversocket.bind((socket.gethostname(), port))
			serversocket.listen(5)
			while 1:
				print "server ready!"
				(clientsocket, address) = serversocket.accept()
				self.socketList.append(clientsocket)
				clientsocket.send(message)
				thread.start_new_thread(self.shandle, (clientsocket, address))
		finally:
			serversocket.close()
	
	def sendToAll(self, msg):
		for socket in self.socketList:
			socket.send(msg)
		
	def sendToPlayer(self, playername, msg):
		socket = self.name2sock[playername]
		socket.send(msg)
		




if __name__ == "__main__":
	server = Server()
	thread.start_new_thread(server.serve, (PORT, "!serverRequest name",))
	
	server.mainloop()
