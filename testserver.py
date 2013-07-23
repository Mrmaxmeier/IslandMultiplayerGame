import socket
import thread

def handle(sock, addr):
	print "connected to", addr
	while 1:
		print addr, ":", sock.recv(1024)

def serve(port, message):
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind((socket.gethostname(), port))
	serversocket.listen(5)
	while 1:
		print "server ready!"
		(clientsocket, address) = serversocket.accept()
		clientsocket.send(message)
		thread.start_new_thread(handle, (clientsocket, address))

def testclient(addr):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(addr)
	thread.start_new_thread(handle, (sock, addr))
	while 1:
		msg = raw_input("Message: ")
		sock.send(msg)
