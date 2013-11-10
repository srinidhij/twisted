import select
import socket
from platform import platform
from time import sleep
from random import random, choice, randint
import string

def genrandstr():
    l = randint(5,100)
    return ''.join([choice(string.ascii_lowercase) for i in xrange(l)])

class epolludpsend:

    def __init__(self):
        try : 
            self.commsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.commsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.commsock.setblocking(0)
            self.fileno = self.commsock.fileno()
            self.epoll = select.epoll()
            self.epoll.register(self.fileno, select.EPOLLOUT)

        except :
            raise
    def send(self, addr, data):
        bwriten = 0
        try :
            events = self.epoll.poll(0)
            for fileno, event in events:
                if event & select.EPOLLOUT:
                    bwriten = self.commsock.sendto(data, addr)
        finally:
            #self.epoll.unregister(self.fileno)
            #self.epoll.close()
            #self.commsock.close()
            pass
        return bwriten 


class polludpsend:
    
    def __init__(self):
        poll = select.poll()
        #poll.register()

    def send(self, data):
        pass

class kqueueudpsend:
    
    def __init__(self):
        self.kqueue = select.kqueue
        self.kevent = select.kevent
        self.commsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.commsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.commsock.setblocking(0)
        self.fileno = self.commsock.fileno()
        self.kq = self.kqueue()
        self.event = [self.kevent(self.fileno, filter=select.KQ_FILTER_WRITE, flags=select.KQ_EV_ADD)]

        self.events = self.kq.control(self.event, 0, 0)
        #poll.register()

    def send(self, addr, data):
        bwriten = 0
        try:
            w_events = self.kq.control(None,4)
            for event in w_events:
                if event.filter == select.KQ_FILTER_WRITE:
                    bwriten = self.commsock.sendto(data, addr)
        finally:
            #self.commsock.shutdown(SHUT_WR)
            #self.commsock.close()
            pass
        return bwriten

def getsender():
    if platform.isLinux():
        try:
            return epolludpsend()
        except:
            return polludpsend()

    elif platform.getType() == 'posix' and not platform.isMacOSX():
        return polludpsend()

    elif platform.isMacOSX():
        try:
            return kqueueudpsend()
        except:
            raise
            return polludpsend()
    else:
        return polludpsend()


sender = getsender()

def send(addr, data):
    sender.send(addr, data)

def tests():
    addr = ('localhost', 8888)
    while  True:
        sleep(random())
        send(addr , genrandstr())

if __name__ == '__main__':
    tests()