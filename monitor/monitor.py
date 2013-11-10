import select
import time
import socket
from platform import platform

BUF_SIZE = 1024*1024
class epolludprecieve:

    def __init__(self, addr):
        try : 
            self.commsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.commsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.commsock.setblocking(0)
            self.commsock.bind(addr)
            self.fileno = self.commsock.fileno()
            self.epoll = select.epoll()
            self.epoll.register(self.fileno, select.EPOLLIN)

        except :
            raise

    def recieve(self):
        data = None
        try :
            events = self.epoll.poll(0)
            for fileno, event in events:
                if event & select.EPOLLIN:
                    data, addr = self.commsock.recvfrom(BUF_SIZE)
        except ValueError:
            raise
        except KeyboardInterrupt:
            #self.epoll.unregister(self.fileno)
            #self.epoll.close()
            #self.commsock.close()
            return data
        finally:
            #self.epoll.unregister(self.fileno)
            #self.epoll.close()
            #self.commsock.close()
            pass
        return data 


class polludprecieve:
    
    def __init__(self):
        poll = select.poll()
        #poll.register()

    def recieve(self, data):
        pass

class kqueueudprecieve:
    
    def __init__(self, addr):
        self.kqueue = select.kqueue
        self.kevent = select.kevent
        self.commsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.commsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.commsock.setblocking(0)
        self.commsock.bind(addr)
        self.fileno = self.commsock.fileno()
        self.kq = self.kqueue()
        self.event = [self.kevent(self.fileno, filter=select.KQ_FILTER_READ, flags=select.KQ_EV_ADD)]

        self.events = self.kq.control(self.event, 0, 0)
        #poll.register()

    def recieve(self):
        data = None
        try:
            r_events = self.kq.control(None,4)
            for event in r_events:
                if event.filter == select.KQ_FILTER_READ:
                    data, addr = self.commsock.recvfrom(BUF_SIZE)
        finally:
            #self.commsock.shutdown(SHUT_WR)
            #self.commsock.close()
            pass
        return data

def getreciever(addr):
    if platform.isLinux():
        try:
            return epolludprecieve(addr)
        except:
            return polludprecieve(addr)

    elif platform.getType() == 'posix' and not platform.isMacOSX():
        return polludprecieve(addr)

    elif platform.isMacOSX():
        try:
            return kqueueudprecieve(addr)
        except:
            raise
            return polludprecieve(addr)
    else:
        return polludprecieve(addr)


addr = ('localhost', 8888)
reciever = getreciever(addr)

def recieve():
        return reciever.recieve()

def tests():
    i = 0
    while  True:
        '''
        print 'before'
        data = recieve()
        print data
        if data is not None :
            pass
            #break
        '''
        data = recieve()
        if data is not None:
            dat = time.ctime() + '::' +data + '\n'
            with open("test.txt", "a") as mfile:
                mfile.write(dat)
        '''
        print 'after , i=',i
        i += 1
        '''
if __name__ == '__main__':
    tests()