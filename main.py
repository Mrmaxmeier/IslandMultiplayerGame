from pybonjourutil import *
import thread
import time


username = raw_input("Username: ")
status = "Online"
port = 1337

user = {}


def bonjourThread(username, port):
	register(username,"_chat._tcp.",port)


def fetch_servers():
	serverlist = list_current("_chat._tcp.")
	#print serverlist
	print
	for [type, name, port, ip] in serverlist:
		username = type.split("._")[0]
		print username+" on Host "+str(name)+" at "+str(ip)+":"+str(port)+" is avalible."
		
		user[username] = [ip, port]
	print user
	
	del user[username]



# Create two threads as follows
try:
	running = True
	thread.start_new_thread(bonjourThread, (username, port, ) )
	while running:
		fetch_servers()
		time.sleep(10)
except Exception as e:
	print "Error: unable to start thread"
	print e
	

while 1:
	pass