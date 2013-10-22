from twisted.web import server, resource
from twisted.internet import reactor

class HelloResource(resource.Resource):
    def __init__(self):
        #super(resource.Resource, self).__init__()
        self.isLeaf = True
        self.numberRequests = 0
    
    def render_GET(self, request):
        self.numberRequests += 1
        request.setHeader("content-type", "text/plain")
        print 'request #',numberRequests
        return "I am request #" + str(self.numberRequests) + "\n"+str(request)

def main(): 
    reactor.listenTCP(8888, server.Site(HelloResource()))
    reactor.run()

if __name__ == '__main__':
    main()