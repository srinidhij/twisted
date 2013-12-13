import socket
from time import sleep

class Sender:
    def __init__(self):
        try:
            self.commsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.commsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.commsock.setblocking(0)
        except Exception as e:
            sys.stderr.write(str(e))

    def send(self, data, addr=None):
        if addr is None:
            addr = ('localhost', 8888)
        self.addr = addr
        bwritten = self.commsock.sendto(data, self.addr)
        return bwritten

    def __exit__(self, type, value, traceback):
        self.commsock.close()


transport = Sender()

def send(data, addr):
    transport.send(data, addr)

def tests():
    from utils import sleeptime, genrandstr
    addr = ('localhost', 8888)
    while  True:
        sleep(sleeptime())
        send(str(genrandstr()), addr)

if __name__ == '__main__':
    tests()