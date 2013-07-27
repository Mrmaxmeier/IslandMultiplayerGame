import string

DEBUG = True

def sendToAll(msg):		print msg		#DEBUG
def sendToOps(msg):		print msg		#DEBUG
def sendToPlayer(s, msg):	print "-->"+s+": "+msg	#DEBUG




class clientCommandHandlerObj():
	def __init__(self, clientObj):
		self.cObj = clientObj
		self.type = "client"
		self.displayMsg = self.cObj.displayMsg
		self.sendToServer = self.cObj.sendToServer
		
	
	def clientSideCmdParse(self, cmd):
		cmd = cmd.split(" ")
	
	
		cmdBase = cmd[0]
		cmd.remove(cmdBase)
		args = cmd
	
		for i in range(99):
			args.append("none")
	
		if cmdBase == "serverRequest":
			if args[0] == "name":
				self.sendToServer(self.cObj.player.name)
			else:
				pass
			
	
	
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
			args.append("none")
	
		if cmdBase == "leave":
			self.sendToAll("[-] "+sender+" left.")
		elif cmdBase == "join":
			self.sendToAll("[+] "+sender+" joined.")
		elif cmdBase == "suicide":
			self.sendToPlayer(sender, "!death")
		elif cmdBase == "death":
			if args[0] == "void" and args[1] == "none":
				self.sendToAll("[=] "+sender+" fell out of the World.")
			elif args[0] == "void":
				self.sendToAll("[=] "+sender+" fell out of the World, thrown by "+args[1]+".")
			else:
				self.sendToAll("[=] "+sender+" died.")
	
		elif cmdBase == "msg":
			self.sendToPlayer(sender, sender+" --> "+args[0]+": "+args[1])
			self.sendToPlayer(args[0], sender+" --> "+args[0]+": "+args[1])
	
		elif cmdBase == "help":
			self.sendToPlayer(sender, "HELPTEXT\nNEWLINE\nStuff\nTEST")
	
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