from random import random, choice, randint
import string

events = ['listenTCP', 'connectTCP', 'listenSSL', 'connectionLost', 'spawnProcess', 'listenUDP']
levels = ['info', 'critical', 'warning']

def genrandstr():
    l = randint(5,20)
    return { 'event': choice(events),
    'msg' : ''.join([choice(string.ascii_lowercase) for i in xrange(l)]), 
    'level' : choice(levels)
    }

def sleeptime(scale=3):
    return scale*random()
