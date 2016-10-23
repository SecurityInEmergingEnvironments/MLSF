import Pyro4
from MLSF import MLSF
from collectors.randomCollectors import *
from simConfig import simConfig

# connect to MLSF server
mlsfServer = Pyro4.Proxy("PYRONAME:mlsfDaemon")

# list simulations currently running on that server
print mlsfServer.listSims()

# create a new simulation on server, named 'sim' using configuration 'simConfig'
# realSimID is the name that is given to the simulation if the name 'sim' is already taken
# mlsf is a pyro4 proxy to the simulation instance that was spun up.
realSimID, mlsf = mlsfServer.newSim( 'sim', config=simConfig, trainingRatio= 0.23 )

# send some data to the simulation as peer named 'noPeer'
# returns the classification of the data
print mlsf.sendData( 'noPeer', [ 2.0, 2.0 ] )

# run the evaluation dataset through the simulation and save results
# evaluation dataset is derived from trainingRatio argument, pulled from dataCollector
# OR passed through using the DEval parameter
mlsf.eval()

# create a report on the MLSF simluation that was run to the current point in time.
mlsf.report()

# list all simulations that are now present on the server
print mlsfServer.listSims()




#?
def remoteSim( serverAddress ):
    server =  Pyro4.Proxy("PYRONAME:mlsfDaemon")

