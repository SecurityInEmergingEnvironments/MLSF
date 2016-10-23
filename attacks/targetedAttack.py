# This module contains the code to conduct a targeted attack on a single datapoint.
# TODO: automatically find victim point and attack point

# NOTE: Currently only works for random linear collector default collector due to
#       hardcoded attack and victim point

from MLAlgorithms.MLAlgorithm import *
#from MLSF.collectors import matLabCollector
import numpy as np
from collectors.dataCollector import *

class targetedAttack( dataCollector ):

    def __init__( self, trainingData=[], algorithm=MLAlgorithm, algArgs={},
                  appArgs={}, *args, **kwargs ):
        dataCollector.__init__( self, *args, **kwargs )

        self.batch = []
        if 'bs' in appArgs.keys():
            self.bSize = appArgs[ 'bs' ]
        else:
            # is this good default functionality?
            self.bSize = 10
        self.algorithm = algorithm( **algArgs['params'] )
        
        self.trainingData=algArgs[ 'params' ][ 'trainingData' ]

        # keep a record of data that has been sent to an app, in what order, what round.
        self.attackHistory={}
        
        # set up the attack
        self.setup( algArgs )
    
    def setup( self, algArgs={} ):
        '''generate attack data and set up attack strategy'''
        
        self.victimPoint = [1.3, 2.0]

        if self.debug: print 'victim point: ', self.victimPoint
        
        self.victimLabel = self.algorithm.classify( self.victimPoint )
        if self.debug: print 'victim label: ', self.victimLabel
        
        self.attackPoint = [ 0.1, 1.1 ]
        if self.debug: print 'start point: ', self.attackPoint

        self.attackLabel = self.algorithm.classify( self.attackPoint )
        if self.debug: print 'attack label: ', self.attackLabel

        self.m, self.b = np.polyfit( [self.victimPoint[0], self.attackPoint[0]], [self.victimPoint[1], self.attackPoint[1]], 1 )

        self.polynomial = np.poly1d([ self.m, self.b ])


    def findNearest( self, label, point ):
        "given a label and point, find the nearest sample of the opposite label"
        if label != self.algorithm.classify( [ 0.9, 0.5 ] ):
            return [ 0.9, .5 ]
        else:
            return [ 3.1, 1.9 ]

    def produceSample( self, s=.02 ):
        if self.bSize > 0:
            if len( self.batch ) > 0 and len( self.batch ) < self.bSize:
                # if this is a batch training algorithm,
                # work around bug in scikit by adding a data
                # point minutely different from the original
                self.attackPoint = [ self.attackPoint[ 0 ] + .0000001, self.polynomial( self.attackPoint[ 0 ] + .0000001 ) ]
                self.batch.append( [ self.attackPoint, self.attackLabel ] )
                if len( self.batch ) == self.bSize:
                    self.algorithm.train( self.batch )
                    self.batch = []
                return self.attackPoint
        
        Xvictim = float(self.victimPoint[0])

        Xattack = float(self.attackPoint[0])
        

        diff = float(Xvictim) - float( Xattack )

        testPoint = self.attackPoint

        testLabel = self.algorithm.classify( [ testPoint ] )
        while diff > s:

            step = diff/float(2)
        
            xTest = float( Xattack ) + step

            testPoint = [ xTest, self.polynomial( xTest ) ]
            testLabel = self.algorithm.classify( testPoint )
            
            if self.debug: print 'testPoint: ', testPoint
            # move back temporary victim point
            if testLabel == self.victimLabel:
                Xvictim = xTest
            else:
                Xattack = xTest
                self.attackPoint = testPoint

            diff = float( Xvictim ) - float( Xattack )
        
        self.batch.append( [ testPoint, testLabel ] )
        return testPoint

    def testDone( self ):
        if not self.algorithm.classify( self.victimPoint ) == self.victimLabel:
            return True

