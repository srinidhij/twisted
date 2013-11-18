from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor
import sys


resource = sys.argv[1] if len(sys.argv) > 1 else File('/Users/srinidhi')
factory = Site(resource)
reactor.listenTCP(8888, factory)
reactor.run()
