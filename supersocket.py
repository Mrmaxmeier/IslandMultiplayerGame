import socket

class SuperSocket:
	def __init__(self, sock):
		self.sock = sock
		self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		self.inBuf = ""
	
	def send(self, msg):
		self.sock.send(msg + "\0")
	
	def recv(self, chsize):
		while not "\0" in self.inBuf:
			self.inBuf += self.sock.recv(chsize)
		msg, _, self.inBuf = self.inBuf.partition("\0")
		return msg
