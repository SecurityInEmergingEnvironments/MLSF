'''
    Example of how to implement a custom attack against an incrementally learning
    algorithm.

    shows ability to add custom visualization and evaluation results to
    reporting functionality

    Shows modification of the default simulation configuration

    Shows the use of a local peer sending data to MLSF

'''

from MLSF import MLSF
from collectors.randomCollectors import *
from simConfig import simConfig
from peers.peer import peer
from attacks.targetedAttack import targetedAttack
import numpy as np
import matplotlib.pyplot as plt

def _Z( _, algorithm ):
    xx, yy = np.meshgrid(np.linspace(0, 2, 200), np.linspace(0, 2, 200))
    Z = algorithm.model.decision_function( np.c_[xx.ravel(), yy.ravel()] )
    Z = Z.reshape(xx.shape)
    return Z

def _samples( _, algorithm ):
    return algorithm.samples

def DecBoundary( results ):
    i = min( results.keys() ) 
    Z = results[ i ][ '_Z' ]
    xx, yy = np.meshgrid(np.linspace(0, 2, 200), np.linspace(0, 2, 200))
    plt.pcolormesh( xx, yy, -Z, cmap=plt.cm.RdBu )
    plt.xticks(())
    plt.yticks(())
    plt.axis('tight')
    for i in results.keys():
        Z = results[ i ][ '_Z' ]
        plt.contour( xx, yy, Z, levels=[0], colors='k' )
    i = max( results.keys() )
    samples = results[ i ][ '_samples' ]
    X, Y = [], []
    for x, y in samples:
        X.append( x )
        Y.append( y )
    plt.scatter( X, Y, cmap=plt.cm.RdBu_r )
    plt.show()


# modify default simulation configuration.
# could also create own simConfig for mlsf.

simConfig[ 'Application' ][ 'params' ][ 'evalMethods' ] = [ _Z, _samples ]
simConfig[ 'Algorithm' ][ 'params' ][ 'debug' ] = False

mlsf = MLSF( config=simConfig, trainingRatio= 0.23, vizFunctions=[DecBoundary] )

mlsf.eval()

trainingData = mlsf.getTrainingData()
algArgs = simConfig['Algorithm']
appArgs = simConfig[ 'Application' ][ 'params' ]

attackPeer = peer( 'attackPeer', trainingData=trainingData, dataCollector=targetedAttack, algArgs=algArgs, appArgs=appArgs, mlsf=mlsf )

for x in range( 5 ):
    for y in range( 10 ):
        # sample is the sample that was sent, response contains a dict mapping data sent back by app
        sample, response = attackPeer.sendSample()

    mlsf.eval()

# create a report on the MLSF simluation that was run to the current point in time.
# Report is generated based on the evalMethods run in 
mlsf.report()

