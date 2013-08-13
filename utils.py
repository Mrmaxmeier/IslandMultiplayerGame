import socket
import pymunk

class SuperSocket:
	def __init__(self, sock):
		self.sock = sock
		self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		self.inBuf = ""
		self.isAlive = True
	
	def send(self, msg):
		try:
			self.sock.send(msg + "\0")
		except:
			self.isAlive = False
			return None
	
	def recv(self, chsize):
		try:
			while not "\0" in self.inBuf:
				recvd = self.sock.recv(chsize)
				if not recvd: raise Exception()
				self.inBuf += recvd
		except:
			self.isAlive = False
			return None
		msg, _, self.inBuf = self.inBuf.partition("\0")
		return msg

class SuperSpace(pymunk.Space):
	def add(self, *objs):
		def f(obj):
			pymunk.Space.add(self, obj)
		for obj in objs:
			self.add_post_step_callback(f, obj)
	
	def remove(self, *objs):
		def f(obj):
			pymunk.Space.remove(self, obj)
		for obj in objs:
			self.add_post_step_callback(f, obj)
