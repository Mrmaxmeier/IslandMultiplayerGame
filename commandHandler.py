import string

DEBUG = True

def sendToAll(msg):       print msg              #DEBUG
def sendToOps(msg):       print msg              #DEBUG
def sendToPlayer(s, msg): print "-->"+s+": "+msg #DEBUG



def serverSideCmdParse(cmd, sender):
	cmd = cmd.split(" ")
	
	
	cmdBase = cmd[0]
	cmd.remove(cmdBase)
	args = cmd
	
	for i in range(99):
		args.append("none")
	
	if cmdBase == "leave":
		sendToAll("[-] "+sender+" left.")
	elif cmdBase == "join":
		sendToAll("[+] "+sender+" joined.")
	elif cmdBase == "suicide":
		sendToPlayer(sender, "!death")
	elif cmdBase == "death":
		if args[0] == "void" and args[1] == "none":
			sendToAll("[=] "+sender+" fell out of the World.")
		elif args[0] == "void":
			sendToAll("[=] "+sender+" fell out of the World, thrown by "+args[1]+".")
		else:
			sendToAll("[=] "+sender+" died.")
	
	elif cmdBase == "msg":
		sendToPlayer(sender, sender+" --> "+args[0]+": "+args[1])
		sendToPlayer(args[0], sender+" --> "+args[0]+": "+args[1])
	
	elif cmdBase == "help":
		sendToPlayer(sender, "HELPTEXT\nNEWLINE\nStuff\nTEST")
	
	elif cmdBase == "playerAction":
		pass #queue.addAction([sender,args[0]])
	elif cmdBase == "playerPosition":
		pass #map.playerlist[sender][pos] = args
	elif cmdBase == "clientRequest":
		pass
	elif cmdBase == "heal":
		pass
	elif cmdBase == "DEBUGMODE":
		pass #map.playerlist[sender][mode] = "DEBUG"
	
	
	
	
	else:
		sendToPlayer(sender, "Could not recognize your Command: !"+cmdBase)




def serverIncomingMsg(msg, sender):
	if msg.startswith("!"):
		sendToOps("-!- "+sender+": "+msg)
		serverSideCmdParse(msg[1:], sender)
	else:
		sendToAll(sender+": "+msg)



sender = "Mrmaxmeier"
while DEBUG:
	#sender = raw_input("Msg from -> ")
	msg = raw_input("Msg from "+sender+"-> ")
	serverIncomingMsg(msg, sender)