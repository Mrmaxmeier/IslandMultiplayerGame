from pybonjourutil import *
import thread
import time

from testserver import serve, testclient


username = raw_input("Username: ")
status = "Online"
port = 1337

user = {}


mainThread = "fetch"


def bonjourThread(username, port):
	register(username,"_chat._tcp.",port)


def fetch_servers():
	user = {}
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



# Create two threads as follows
try:
	running = True
	thread.start_new_thread(serve, (port+1, "Helllo, World!"))
	thread.start_new_thread(bonjourThread, (username, port, ) )
	time.sleep(2)
	while running:
		if mainThread == "fetch":
			print
			fetch_servers()
			print
		time.sleep(10)
except Exception as e:
	print "Error: unable to start thread"
	print e
	

while 1:
	pass