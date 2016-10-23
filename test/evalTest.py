'''
    Simple test that adds a custom metric to our results.

    This metric function is called every time mlsf.eval() is called.

    the default implementation of mlsf.report() will display the metrics
    collected for each mlsf.eval() call
'''

from MLSF import MLSF
from collectors.randomCollectors import *
from simConfig import simConfig

# returns number of samples algorithm trains on so far as well as number of samples in data
def testMetric( data, algorithm ):
    return str( len(data) ) + ':' + str( len( algorithm.samples ) )

simConfig['Application']['params']['evalMethods'] = [ testMetric ]

mlsf = MLSF( simConfig, trainingRatio=.43 )
mlsf.eval()
mlsf.report()
