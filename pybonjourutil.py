import select
import socket
import sys
import pybonjour




def register_callback(sdRef, flags, errorCode, name, regtype, domain):
	if errorCode == pybonjour.kDNSServiceErr_NoError:
		print 'Registered service:'
		print '  name	=', name
		print '  regtype =', regtype
		print '  domain  =', domain

def register(name, regtype, port):
	sdRef = pybonjour.DNSServiceRegister(name = name,
		regtype = regtype,
		port = port,
		callBack = register_callback)
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





















def query_record_callback(sdRef, flags, interfaceIndex, errorCode, fullname,
						  rrtype, rrclass, rdata, ttl):
	if errorCode == pybonjour.kDNSServiceErr_NoError:
		print '  IP		 =', socket.inet_ntoa(rdata)
		queried.append(True)


def resolve_callback(sdRef, flags, interfaceIndex, errorCode, fullname,
					 hosttarget, port, txtRecord):
	if errorCode != pybonjour.kDNSServiceErr_NoError:
		return

	print 'Resolved service:'
	print '  fullname   =', fullname
	print '  hosttarget =', hosttarget
	print '  port	   =', port

	query_sdRef = \
	pybonjour.DNSServiceQueryRecord(interfaceIndex = interfaceIndex,
		fullname = hosttarget,
		rrtype = pybonjour.kDNSServiceType_A,
		callBack = query_record_callback)

	try:
		while not queried:
			ready = select.select([query_sdRef], [], [], timeout)
			if query_sdRef not in ready[0]:
				print 'Query record timed out'
				break
			pybonjour.DNSServiceProcessResult(query_sdRef)
		else:
			queried.pop()
	finally:
		query_sdRef.close()

	resolved.append(True)


def browse_callback(sdRef, flags, interfaceIndex, errorCode, serviceName,
					regtype, replyDomain):
	if errorCode != pybonjour.kDNSServiceErr_NoError:
		return

	if not (flags & pybonjour.kDNSServiceFlagsAdd):
		print 'Service removed'
		return

	print 'Service added; resolving'

	resolve_sdRef = pybonjour.DNSServiceResolve(0,
		interfaceIndex,
		serviceName,
		regtype,
		replyDomain,
		resolve_callback)

	try:
		while not resolved:
			ready = select.select([resolve_sdRef], [], [], timeout)
			if resolve_sdRef not in ready[0]:
				print 'Resolve timed out'
				break
			pybonjour.DNSServiceProcessResult(resolve_sdRef)
		else:
			resolved.pop()
	finally:
		resolve_sdRef.close()

resolved = []
timeout  = 5
queried  = []

def browse_resolve_query(regtype, timeout  = 5, queried  = [], resolved = []):
	browse_sdRef = pybonjour.DNSServiceBrowse(regtype = regtype,
		callBack = browse_callback)

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
