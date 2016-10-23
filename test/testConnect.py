'''
    Test ability to connect to a remote MLSF instance via the server
    it is run on.
    Requirements to run:
        - run python -m MLSFServer localhost to start server
'''

import Pyro4

mlsfServer = Pyro4.Proxy("PYRONAME:mlsfDaemon")
simName, _mlsf = mlsfServer.newSim( 'sim2' )

mlsfName = simName

mlsf = mlsfServer.connect( mlsfName )

print 'sending data to simulation...'
print 'classified as', mlsf.sendData( 'noPeer', [ 2.0, 2.0 ] )
mlsf.eval()
mlsf.report()

