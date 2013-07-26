from commandHandler import *
from player import *


class Server():
	def __init__(self):
		self.players = []	#[PlayerObj, PlayerObj...]
		self.map = []		#[Island, Island...]
		self.chatLog = []	#[["Sender","Message","Timestamp"]]
		self.unprocessedChat= []#[["Sender","Message","Timestamp"]]
		self.cmdObj = CommandHandlerObj()
	
	def tick(self):
		if self.unprocessedChat:
			for sender, cmd, timestamp in self.unprocessedChat:
			self.cmdObj.serverIncomingMessage(sender, cmd)
			self.chatLog.append([sender, cmd, timestamp])
	
		