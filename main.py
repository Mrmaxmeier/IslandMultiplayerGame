from pybonjourutil import *
import thread


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

fetch_servers()


# Create two threads as follows
try:
   thread.start_new_thread(bonjourThread, (username, port, ) )
except:
   print "Error: unable to start thread"

while 1:
   pass