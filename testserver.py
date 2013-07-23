import socket
import thread

def handle(sock, addr, message):
	print "connected to", addr
	sock.send(message)
	while 1:
		print addr, ":", sock.recv(1024)

def serve(port, message):
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind((socket.gethostname(), port))
	serversocket.listen(5)
	while 1:
		print "server ready!"
		(clientsocket, address) = serversocket.accept()
		thread.start_new_thread(handle, (clientsocket, address, message))
