import select
import socket
import sys
import pybonjour






def register(name, regtype, port):
	sdRef = pybonjour.DNSServiceRegister(name = name,
		regtype = regtype,
		port = port,
		callBack = ezCallbackobj.register_callback)
	try:
		try:
			while True:
				ready = select.select([sdRef], [], [])
				if sdRef in ready[0]:
					pybonjour.DNSServiceProcessResult(sdRef)
		except KeyboardInterrupt:
			pass
	finally:
		sdRef.close()








class ezCallback():
	def __init__(self):
		self.resolvedData = []
		self.resolved = []
		self.timeout  = 5
		self.queried  = []
		self.silent = True

	def register_callback(self, sdRef, flags, errorCode, name, regtype, domain):
		if errorCode == pybonjour.kDNSServiceErr_NoError and not self.silent:
			print 'Registered service:'
			print '  name	=', name
			print '  regtype =', regtype
			print '  domain  =', domain

	def query_record_callback(self, sdRef, flags, interfaceIndex, errorCode, fullname,
							  rrtype, rrclass, rdata, ttl):
		if errorCode == pybonjour.kDNSServiceErr_NoError:
			if not self.silent:
				print '  IP		 =', socket.inet_ntoa(rdata)
			self.resolvedData[-1].append(socket.inet_ntoa(rdata))
			self.queried.append(True)


	def resolve_callback(self, sdRef, flags, interfaceIndex, errorCode, fullname,
						 hosttarget, port, txtRecord):
		if errorCode != pybonjour.kDNSServiceErr_NoError and not self.silent:
			return

		if not self.silent:
			print 'Resolved service:'
			print '  fullname   =', fullname
			print '  hosttarget =', hosttarget
			print '  port	    =', port
			#print '  txtrecord  =', txtRecord
	
		self.resolvedData.append([fullname, hosttarget, port])

		query_sdRef = \
		pybonjour.DNSServiceQueryRecord(interfaceIndex = interfaceIndex,
			fullname = hosttarget,
			rrtype = pybonjour.kDNSServiceType_A,
			callBack = self.query_record_callback)

		try:
			while not self.queried:
				ready = select.select([query_sdRef], [], [], self.timeout)
				if query_sdRef not in ready[0]:
					if not self.silent:
						print 'Query record timed out'
					break
				pybonjour.DNSServiceProcessResult(query_sdRef)
			else:
				self.queried.pop()
		finally:
			query_sdRef.close()

		self.resolved.append(True)


	def browse_callback(self, sdRef, flags, interfaceIndex, errorCode, serviceName,
						regtype, replyDomain):
		if errorCode != pybonjour.kDNSServiceErr_NoError:
			return

		if not (flags & pybonjour.kDNSServiceFlagsAdd):
			if not self.silent:
				print 'Service removed'
			return

		if not self.silent:
			print 'Service added; resolving'
	
	

	
	
		resolve_sdRef = pybonjour.DNSServiceResolve(0,
			interfaceIndex,
			serviceName,
			regtype,
			replyDomain,
			self.resolve_callback)
	
		#print(resolve_sdRef)

		try:
			while not self.resolved:
				ready = select.select([resolve_sdRef], [], [], self.timeout)
				if resolve_sdRef not in ready[0]:
					if not self.silent:
						print 'Resolve timed out'
					break
				pybonjour.DNSServiceProcessResult(resolve_sdRef)
			else:
				self.resolved.pop()
		finally:
			resolve_sdRef.close()

ezCallbackobj = ezCallback()

def browse_resolve_query(regtype, timeout  = 5, queried  = [], resolved = []):
	browse_sdRef = pybonjour.DNSServiceBrowse(regtype = regtype,
		callBack = ezCallbackobj.browse_callback)

	try:
		try:
			while True:
				ready = select.select([browse_sdRef], [], [])
				if browse_sdRef in ready[0]:
					pybonjour.DNSServiceProcessResult(browse_sdRef)
		except KeyboardInterrupt:
			pass
	finally:
		browse_sdRef.close()











def list_current(regtype):
	browse_sdRef = pybonjour.DNSServiceBrowse(regtype = regtype,
		callBack = ezCallbackobj.browse_callback)
	

	
	try:
		try:
			for i in [0]:
				ready = select.select([browse_sdRef], [], [])
				if browse_sdRef in ready[0]:
					pybonjour.DNSServiceProcessResult(browse_sdRef)
		except KeyboardInterrupt:
			pass
	finally:
		browse_sdRef.close()
	
	resolvedData = ezCallbackobj.resolvedData
	ezCallbackobj.resolvedData = []
	return resolvedData
