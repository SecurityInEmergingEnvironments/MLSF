from collectors.dataCollector import *
from attacks import *
import threading
from time import sleep
from MLAlgorithms.MLAlgorithm import *

class peer( object ):

    _name='defaultPeer'

    def __init__( self, name, server=None, simName=None, *args, **kwargs  ):
        self.setup( *args, **kwargs )

        self.dataSent = []

    def setup( self, mlsf=None, frequency=1, algorithm=MLAlgorithm,
               dataCollector=dataCollector, algArgs={}, appArgs={},
               trainingData=None, name=None, dcargs={}, *args, **kwargs ):

        self.algArgs = algArgs
        self.appArgs = appArgs
        
        # frequency of new data
        self.frequency = frequency

        # initialize our API
        self.name=name

        self.dataSource=dataCollector( trainingData=trainingData, algArgs=algArgs, algorithm=algorithm, appArgs=appArgs, **dcargs )
        
        self.trainingData = trainingData if trainingData else []
        
        self.mlsf = mlsf

        self.running=False
        
        # This is the thread that will produce data and send it to mlsf
        self.dataThread = threading.Thread( target=self.dataFactory )
        

    def start( self, wait=False ):
        self.dataThread.start()
        if wait:
            self.dataThread.join()

    def dataFactory( self ):
        """
           Data production thread in peer.
        """
        a = 0
        if not self.mlsf:
            print self.name, ': not connected to any MLSF instance'
            self.running = False
        while self.running:
            sleep( self.frequency )
            sample, response = self.sendSample()
            print 'dataFactory Working:'
            print 'sending sample: ', sample
            print 'label trained: ', response[ 'label' ]

    def newSample( self ):
        sample = self.dataSource.produceSample()
        self.dataSent.append( sample )
        return sample

    def sendSample( self ):
        sample = self.newSample()
        response = self.mlsf.sendData( self.name, sample )
        return sample, response
