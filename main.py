from pybonjourutil import *
import thread
import time

from testserver import serve, testclient


username = raw_input("Username: ")
status = "Online"
port = 1337
serverport = 7331
protocol = "_chat._tcp"

user = {}


DEBUG = True


mainThread = "fetch"


def bonjourThread(username, port):
	register(username,"_chat._tcp.",port)


def fetch_servers():
	for key in user.keys():
		del user[key]
	
	
	serverlist = list_current("_chat._tcp.")
	#print serverlist
	print
	for [type, name, port, ip] in serverlist:
		curusername = type.split("._")[0]
		print curusername+" on Host "+str(name)+" at "+str(ip)+":"+str(port)+" is avalible."
		
		user[str(curusername)] = [ip, port]
	try:
		del user[username]
	except:
		print "Fetched before registered."
	print user


def askforConn():
	print
	print "0: Pass"
	c = 0
	for name in user.keys():
		c += 1
		ip, port = user[name]
		print str(c)+": "+name+" on "+ip+":"+str(serverport)
	print
	choice = int(raw_input("Connect to: "))-1
	
	
	print
	
	
	return user.keys()[choice]


# Create two threads as follows
try:
	running = True
	thread.start_new_thread(serve, (serverport, "Helllo, World!"))
	thread.start_new_thread(bonjourThread, (username, port, ) )
	thread.start_new_thread(scanner_handler, (protocol,))
	time.sleep(2)
	while running:
		if mainThread == "fetch":
			print
			fetch_servers()
			print
		time.sleep(10)
		if len(user) > 0:
			running = False
	
	curruserOld = "LOL"
	
	while DEBUG:
		
		if ezCallbackobj.currUser != curruserOld:
			print
			print ezCallbackobj.currUser
		
		if ezCallbackobj.userActions:
			print ezCallbackobj.userActions[0]
			ezCallbackobj.userActions.remove(ezCallbackobj.userActions[0])
		curruserOld = ezCallbackobj.currUser
	
	name = askforConn()
	[ip, port] = user[name]
	
	print "Connecting to "+name+" on "+ip+":"+str(serverport)
	
	testclient((ip,serverport))
	
except Exception as e:
	print "Error: unable to start thread"
	print e
	

while 1:
	pass
