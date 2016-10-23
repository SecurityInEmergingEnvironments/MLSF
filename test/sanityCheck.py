'''
    Sanity check that local MLSF instance allows us to send data, then report
    on the data after it is trained and evaluated.
'''

from MLSF import MLSF
from simConfig import simConfig
from collectors.randomCollectors import *

mlsf = MLSF( simConfig, trainingRatio=0.47 )

mlsf.eval()

coll = randomLinear()

for i in range (34):
    mlsf.sendData( 'testPeer', coll.produceSample() )

mlsf.eval()

mlsf.report()
