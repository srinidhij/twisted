import sys
import select
import socket
from platform import platform
from time import sleep

class EPollNotImplemented(Exception):
    ''' Exception class for epoll not being supported 
    for the platform'''
    pass

class KQueueNotImplemented(Exception):
    ''' Exception class for kqueue not being supported 
    for the platform'''
    pass


class epolludpsend:

    def __init__(self):
        try : 
            self.commsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.commsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.commsock.setblocking(0)
            self.fileno = self.commsock.fileno()
            self.epoll = select.epoll()
            self.epoll.register(self.fileno, select.EPOLLOUT)

        except AttributeError:
            raise EPollNotImplemented()

        except Exception, e:
            sys.stderr.write(str(e))

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
        try:
            self.commsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.commsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.commsock.setblocking(0)
            self.commsock.bind(addr)
            self.fileno = self.commsock.fileno()
            self.poll = select.poll()
            self.poll.register(self.fileno, select.POLLOUT)

        except Exception, e:
            sys.stderr.write(str(e))

    def recieve(self, addr, data):
        bwriten = 0
        try:
            events = self.poll.poll(0)
            for fileno, event in events:
                if event & select.POLLOUT:
                    bwriten = self.commsock.sendto(data, addr)
        except ValueError:
            pass
        except KeyboardInterrupt:
            return bwriten
        finally:
            pass
        return bwriten

class kqueueudpsend:
    
    def __init__(self):
        try:
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
        except AttributeError:
            raise KQueueNotImplemented()

        except Exception, e:
            sys.stderr.write(str(e))


    def send(self, addr, data):
        bwriten = 0
        try:
            w_events = self.kq.control(None,4)
            for event in w_events:
                if event.filter == select.KQ_FILTER_WRITE:
                    bwriten = self.commsock.sendto(data, addr)

        except Exception, e:
            sys.stderr.write(str(e))
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
            return polludpsend()
    else:
        return polludpsend()


sender = getsender()

def send(addr, data):
    sender.send(addr, data)

def tests():
    from utils import sleeptime, genrandstr
    addr = ('localhost', 8888)
    while  True:
        sleep(sleeptime())
        send(addr , str(genrandstr()))

if __name__ == '__main__':
    tests()