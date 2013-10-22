import sys
import math
import time
from twisted.python import log

log.startLogging(sys.stdout)
log.msg("Starting experiment")
log.msg("Logging an exception")
try: 
	for i in range(1,100):
		start = time.time()
		j = math.factorial(i)
		j %= 1000
		end = time.time() - start
		msg = 'fact %s = %s, time taken = %ss'%(str(i),str(j),str(end))
		log.msg(msg)	
except Exception, e: 
	log.err(e)
log.msg("Ending experiment")
