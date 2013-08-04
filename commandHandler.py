import string

from player import *

DEBUG = True

def sendToAll(msg):		print msg		#DEBUG
def sendToOps(msg):		print msg		#DEBUG
def sendToPlayer(s, msg):	print "-->"+s+": "+msg	#DEBUG




class clientCommandHandlerObj():
	def __init__(self, clientObj):
		self.cObj = clientObj
		self.cMap = self.cObj.map
		self.cIslands = self.cMap.islands
		self.cSeed2isl = self.cMap.islseed2isl
		self.cName2Player = self.cMap.name2player
		self.cPlayers = self.cMap.players
		
		self.type = "client"
		self.displayMsg = self.cObj.chat.receive
		self.sendToServer = self.cObj.sendToServer
		
	
	def clientSideCmdParse(self, cmd):
		cmd = cmd.split(" ")
	
	
		cmdBase = cmd[0]
		cmd.remove(cmdBase)
		args = cmd
	
		for i in range(9):
			args.append(None)
	
		if cmdBase == "serverRequest":
			#if args[0] == "name":
			#	self.sendToServer(self.cObj.player.name)
			#else:
				pass
		elif cmdBase == "serverInformation":
			if args[0] == "mapSeed":
				self.cMap.seed = float(args[1])
				self.cMap.genIslands()
			elif args[0] == "islandPosition":# seed pos angle
				self.cSeed2isl[float(args[1])].body.position = (float(args[2]),float(args[3]))
				self.cSeed2isl[float(args[1])].body.angle = float(args[4])
				self.cSeed2isl[float(args[1])].body.velocity = (float(args[5]), float(args[6]))
			elif args[0] == "playerPosition":# name pos angle
				self.cName2Player[args[1]].body.position = (float(args[2]),float(args[3]))
				self.cName2Player[args[1]].body.angle = float(args[4])
				self.cName2Player[args[1]].body.velocity = (float(args[5]), float(args[6]))
				#print (args[1]+"'s Position:", 
					#self.cName2Player[args[1]].body.position)

			elif args[0] == "newPlayer":# name pos angle
				if not args[1] in self.cPlayers:
					pos = (float(args[2]),float(args[3]))
					newplayer = Player(pos, self.cMap.space)
					newplayer.name = args[1]
					self.cPlayers.append(newplayer)
					self.cName2Player[args[1]] = newplayer
					self.cName2Player[args[1]].body.position = pos
					self.cName2Player[args[1]].body.angle = float(args[4])
				else:
					print "Player already registred"
			
	
	
	def clientIncomingMsg(self, msg):
		if msg.startswith("!"):
			self.clientSideCmdParse(msg[1:])
			self.displayMsg(msg) #Debug
		else:
			self.displayMsg(msg)






class serverCommandHandlerObj():
	def __init__(self, serverObj):
		self.sObj = serverObj
		self.sMap = self.sObj.map
		self.sIslands = self.sMap.islands
		self.sSeed2isl = self.sMap.islseed2isl
		self.sName2Player = self.sMap.name2player
		self.sPlayers = self.sMap.players
		self.type = "server"
		self.sendToAll = self.sObj.sendToAll
		self.sendToPlayer = self.sObj.sendToPlayer
		
	
	def serverSideCmdParse(self, cmd, sender):
		cmd = cmd.split(" ")
	
	
		cmdBase = cmd[0]
		cmd.remove(cmdBase)
		args = cmd
	
		for i in range(99):
			args.append(None)
	
		if cmdBase == "leave":
			self.sendToAll("[-] "+sender+" left.")
		elif cmdBase == "join":
			self.sendToAll("[+] "+sender+" joined.")
			self.sObj.newPlayer(sender)
		elif cmdBase == "suicide":
			self.sendToPlayer(sender, "!death")
		elif cmdBase == "death":
			if args[0] == "void" and args[1] == None:
				self.sendToAll("[=] "+sender+" fell out of the World.")
			elif args[0] == "void":
				self.sendToAll("[=] "+sender+" fell out of the World, killed by "+args[1]+".")
			else:
				self.sendToAll("[=] "+sender+" died.")
	
		elif cmdBase == "msg":
			if args[0] is None: return self.sendToPlayer(sender, "No Player given!")
			message = " ".join([arg for arg in args[1:] if arg != None])
			try:
				self.sendToPlayer(args[0], sender+" --> "+args[0]+": "+message)
				self.sendToPlayer(sender, sender+" --> "+args[0]+": "+message)
			except KeyError:
				self.sendToPlayer(sender, "Player not found: "+args[0])
	
		elif cmdBase == "help":
			self.sendToPlayer(sender, "HELPTEXT\nNEWLINE\nStuff\nTEST")
		elif cmdBase == "ping":
			print "parsing Ping"
			self.sendToPlayer(sender, "Pong!")
	
		elif cmdBase == "playerAction":
			pass #queue.addAction([sender,args[0]])
		elif cmdBase == "playerPosition":
			player = self.sName2Player[sender]
			x, y, vx, vy = args[:4]
			player.body.position = float(x), float(y)
			player.body.velocity = float(vx), float(vy)
		elif cmdBase == "clientRequest":
			pass
		elif cmdBase == "heal":
			pass
	
		elif cmdBase == "asserver":
			if args[0] is None: return self.sendToPlayer(sender, "No Player given!")
			message = " ".join([arg for arg in args[1:] if arg != None])
			try:
				self.sendToPlayer(args[0], message)
				self.sendToPlayer(sender, "Server"+" --> "+args[0]+": "+message)
			except KeyError:
				self.sendToPlayer(sender, "Player not found: "+args[0])
		
		elif cmdBase == "sudo":
			if args[0] is None: return self.sendToPlayer(sender, "No Player given!")
			message = " ".join([arg for arg in args[1:] if arg != None])
			try:
				self.sendToPlayer(sender, args[0]+": "+message)
				self.serverIncomingMsg(message, args[0])
			except KeyError:
				self.sendToPlayer(sender, "Player not found: "+args[0])
	
		elif cmdBase == "debug":
			print
			print
			print "Parsed !debug from "+sender+", ingame: ", self.sObj.map.name2player[sender]
			print sender+"'s Socket: ", self.sObj.name2sock[sender].sock
			print
			print 'Replying "Got !debug".'
			self.sendToPlayer(sender, "Got !debug")
			print
		
		
		elif cmdBase == "stop":
			print
			print sender+" stopped the Server."
			import sys
			sys.exit()
	
		else:
			self.sendToPlayer(sender, "Could not recognize your Command: !"+cmdBase)

	def serverIncomingMsg(self, msg, sender):
		if msg.startswith("!"):
			#sendToOps("-!- "+sender+": "+msg)
			self.serverSideCmdParse(msg[1:], sender)
		else:
			self.sendToAll(sender+": "+msg)
