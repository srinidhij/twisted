#Reactor metrics and Monitoring interface for Twisted Reactor

##What is this ?

I am building a reporting protocol which would report timings and potentially other relevant status information on the reactor’s activities to a client connected on an appropriate socket. For example: the longest, shortest, mean and median event times over a particular interval, and which objects and code were involved in the longest and shortest. (This would not necessarily involve a user interface, just the internal infrastructure necessary to extract and report this information to other tools which could make sense of it.)



##Why ?

The reactor runs lots of events; connectionMade, dataReceived, connectionLost, timed calls, and queued calls from callFromThread. But currently there’sno tools to discover how long those events took, or what resources they consumed, so when one event makes your reactor gets “stuck” you might not know which one it is without some manual instrumentation.

