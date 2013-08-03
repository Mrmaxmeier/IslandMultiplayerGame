import string

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
			if args[0] == "name":
				self.sendToServer(self.cObj.player.name)
			else:
				pass
		elif cmdBase == "serverInformation":
			if args[0] == "mapSeed":
				self.cMap.seed = args[1]
				self.cMap.genIslands()
			elif args[0] == "islandPosition":# seed pos angle
				self.cSeed2isl[args[1]].body.position = (args[2],args[3])
				self.cSeed2isl[args[1]].body.angle = args[4]
			elif args[0] == "playerPosision":# name pos angle
				if not args[1] == self.cObj.player.name:
					self.cName2Player[args[1]].body.position = (args[2],args[3])
					self.cName2Player[args[1]].body.angle = args[4]
				else:
					print "got OWN Position"
			
	
	
	def clientIncomingMsg(self, msg):
		if msg.startswith("!"):
			self.clientSideCmdParse(msg[1:])
		else:
			self.displayMsg(msg)






class serverCommandHandlerObj():
	def __init__(self, serverObj):
		self.sObj = serverObj
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
			self.sendToPlayer(sender, sender+" --> "+args[0]+": "+args[1])
			self.sendToPlayer(args[0], sender+" --> "+args[0]+": "+args[1])
	
		elif cmdBase == "help":
			self.sendToPlayer(sender, "HELPTEXT\nNEWLINE\nStuff\nTEST")
		elif cmdBase == "ping":
			print "parsing Ping"
			self.sendToPlayer(sender, "Pong!")
	
		elif cmdBase == "playerAction":
			pass #queue.addAction([sender,args[0]])
		elif cmdBase == "playerPosition":
			pass #map.playerlist[sender][pos] = args
		elif cmdBase == "clientRequest":
			pass
		elif cmdBase == "heal":
			pass
	
	
	
	
		else:
			self.sendToPlayer(sender, "Could not recognize your Command: !"+cmdBase)

	def serverIncomingMsg(self, msg, sender):
		if msg.startswith("!"):
			#sendToOps("-!- "+sender+": "+msg)
			self.serverSideCmdParse(msg[1:], sender)
		else:
			self.sendToAll(sender+": "+msg)