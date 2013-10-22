from twisted.internet import protocol, reactor 
from twisted.python import log
import time

class Echo(protocol.Protocol): 
	def dataReceived(self, data):
		msg = 'recieved data %s at t=%s'%(data,str(time.time()))
		log.msg(msg)
        	self.transport.write(data)
		msg = 'sent data  %s at t=%s'%(data,str(time.time()))
		log.msg(msg)

class EchoFactory(protocol.Factory): 
	def buildProtocol(self, addr):
		return Echo()

log.startLogging(open('echo.log', 'w'))
reactor.listenTCP(8000, EchoFactory())
reactor.run()
