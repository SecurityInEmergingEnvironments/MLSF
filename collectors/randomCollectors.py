'''
Using inheritance on generateData, the generateDataStreamLine creates either a tuple of data and a label (training) for that data
or just the tuple to be sent to be predicted (prediction). Bypasses feature extraction component of application.
'''
from dataCollector import *
import random

class randomLinear( dataCollector ):
    
    _name='randomLinear'
    
    def __init__(self, min=0, max=2, name="two class linear ground truth", *args, **kwargs ):
        self.min=min
        self.max=max
        dataCollector.__init__( self, name, *args, **kwargs )
    
    '''
    
      2 #\   
        # \
        #  \ B
      1 # A \
        #    \
      0 ########
        0  1  2
    '''

    def produceSample( self, label=None ):
        "generates data split by the function 'f(x) = -x + 2' "
        # generate a sample that does not fall on the function line
        while True:
            x = random.uniform( self.min, self.max )
            y = random.uniform( self.min, self.max )
            if y != ( ( -1  * x ) + 2 ):
                break
        if label:
            if y > ( ( -1  * x ) + 2 ):
                label = 'B'
            elif y < ( ( -1 * x ) + 2 ):
                label = 'A'
            return  [ label, [ x, y ] ]
        else:
            return  [ x, y ]



#a = linearGroundTruth(name="test")
#for i in range( 20 ):
#    print a.produceSample( )

