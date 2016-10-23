'''
    AUTHORS: Cody Burkard, Julio Perez
    University of Washington, Bothell
    Security in Emerging Environments

    Main MLSF class. This class contains all other elements of the
    framework, and acts as a central controlling/logging class.
    Most other classes reside in Application.
'''

from data import data
from logging import *
from util import *
import json
import Pyro4
from moduleLib import loadComponent
from evaluation import Accuracy
from simConfig import simConfig

@Pyro4.expose
class MLSF( object ):

    def __init__( self, config=simConfig, trainingRatio=1.00, vizFunctions=[], 
                   debugLvl='warning',*args, **kwargs ):
        '''Create a test for a machine learning algorithm or a
           simulation of a machine learning attack
           defense=mitigation technique to use
           dataSource=where to collect data from'''
        self.vizFunctions = vizFunctions

        if type( config ) == str:
            config = json.loads( config )
        self.trainingRatio=trainingRatio # ratio of data that is used for training and data that is used for eval
        self.data = data()
        self.peers = []
        self.plotCounter=0
        self.states=[]
        self.DTrain=[]
        self.DEval=[]
        self.evalCallbacks=[] #callbacks used in application to generate evaluation results
        
        # load all components from our moduleLib.
        # This allows us to pass in strings as our module names, which
        # are easily serializeable for network connecitons
        try:
            self.applicationClass = loadComponent( config[ 'Application' ][ 'name' ] )
            self.appArgs = config[ 'Application' ][ 'params' ]
            self.defenseClass = loadComponent( config[ 'Defense' ][ 'name' ] )
            self.defArgs = config[ 'Defense' ][ 'params' ]
            self.algorithmClass = loadComponent( config[ 'Algorithm' ][ 'name' ] )
            self.algArgs = config[ 'Algorithm' ][ 'params' ]
            self.dataSourceClass = loadComponent( config[ 'dataCollector' ][ 'name' ] )
            self.dsArgs = config[ 'dataCollector' ][ 'params' ]
        except Exception as msg:
            print 'exception occured while loading components'
            print msg
            exit()
        
        self.dataSource=self.dataSourceClass( **self.dsArgs )
        # data source should probably hold on to original training data unless reset.
        # that way, training data is not changing every time this is called
        self.collectedData = self.dataSource.collectTrainingData()

        # Split up collected data into training data and evaluation data
        # INFO: evaluation data should be pulled from same probability distribution
        # as training data in most cases

        # TODO: implement cross validation as eval() method
        trainIndex = int( float( len( self.collectedData ) ) * trainingRatio )
        self.DTrain=self.collectedData[ 0:trainIndex ]
        self.DEval=self.collectedData[ trainIndex: ]

        self.algArgs['trainingData']=self.DTrain

        self.application=self.applicationClass(
            algorithm=self.algorithmClass, algArgs=self.algArgs,
            defense=self.defenseClass, defArgs=self.defArgs,
            **self.appArgs )
        self.data.setTrainingData( self.DTrain )
    
    @Pyro4.expose
    def eval( self, Deval=None, train=False, evalCallbacks=[ Accuracy ] ):
        
        if not Deval: Deval=self.DEval
        if not evalCallbacks:
            evalCallbacks=self.evalCallbacks
    
        # results return a dict of evaluation name and resulting value
        results=self.application.eval( Deval, train, evalCallbacks )
        self.data.saveEval( results )

    # TODO: determine if this is correct functionality?
    # Should data be reinitialized?
    @Pyro4.expose
    def reset( self, algorithm=None, dargs={}, algArgs={}, dcargs={} ):
        self.data = data()
        self.peers = []

        self.application.reset( trainingData=self.DTrain )
        self.data.setTrainingData( self.DTrain )

    @Pyro4.expose
    def setApp( self, app, *args, **kwargs ):
        try:
            self.applicationClass = loadComponent( app )
        except Exception as msg:
            print 'couldnt find app class: %s' % app
            print msg
            exit()
    
    @Pyro4.expose
    def getApp( self ):
        if self.applicationClass:
            return self.applicationClass.__name__
        else:
            return None

    # TODO: implement peer creation
    #       - peer should be spun up on daemon
    #       - communicate with daemon, request new peer?
    def createPeer( self, *args, **kwargs ):
        '''
           Create a peer
        '''
        peerName = 'peer' + str( len( self.peers ) + 1 )
        # finish inplementation

    def getTrainingData( self ):
        "Get training data from dataSource"
        return self.DTrain
        #return self.dataSource.collectTrainingData()

    def sendApp( self, peer, sample, EID, label=None ):
        "Send sample to application. Log data before it is sent"
        sampleResults, response = self.application.send( peer=peer, sampleID=EID,
                                      sample=sample )

        for ID in sampleResults.keys():
            self.data.log( ID, **sampleResults[ ID ] )
        return response

    def sendData( self, peer, sample, label=None ):
        # log data as it is sent to MLSF
        EID = self.data.newEntry( sample, peer=peer, trueLabel=label )
        return self.sendApp( peer, sample, EID, label )

    def queryData( self, attr, val=None ):
        '''
           Query our data object. Private class function
           attr: attribute we are querying on
           val: value we are looking for
        '''
        attrDict = {}
        attrDict[ attr ] = val
        result = self.data.query( **attrDict )
        return result

    def dataLog( self ):
        "Return JSON string of all data in data object. Private"
        result = self.data.rawData()
        return result

    # NOTE: currently unused/unimplemented.
    # Should run a self contained simulation with multiple peers
    # Need to include idea of peers in application first
    def run( self ):
        '''
           run the simulation
        '''
        pass

    def _formatResults( self, results ):
        "format the evaluation results generated by the application and MLSF"

        line = '\n\n*********************************************\n\n'
        resultsString = line
        e=0
        sortedResultKeys = sorted( results.keys() )
        for i in sortedResultKeys:
            e += 1
            stateString = 'state ' + str( e ) + '( %i samples ):' % i
            numDash = len( stateString )
            resultsString += stateString + '\n'
            for _ in range( numDash ):
                resultsString += '_'
            resultsString += '\n\n'

            for metric, value in results[ i ].items():
                if metric[ 0 ] == '_':
                    continue
                resultsString += metric + ': ' + str( value ) + '\r\n'
            resultsString += line
        return resultsString

    # TODO: document visFunction callback
    def report( self, output='stdout', visFunctions=[] ):
        '''
        Overwrite this for a custom report.
        Default report includes evaluation results at all evaluation steps
        as well as a final report containing number of new samples trained
        in each class.
        '''
        # eval results(from every call)
        resultsHeader = 'Final Report:'
        evalResults = self.data.getResults()
        finalResults = self.data.genReport()
        finalResultsString = 'Final Results:\n--------------\n\n'
        for metric, val in finalResults.items():
            finalResultsString += metric + ': ' + str( val ) + '\r\n'
        if output == None:
            return evalResults
        if output == 'stdout':
            resultString = resultsHeader + self._formatResults( evalResults  )
            resultString += finalResultsString
            print resultString
        else:
            print output, 'not yet implemented\n'
            resultString = resultsHeader + self._formatResults( evalResults  )
            resultString += finalResultsString
            print resultString
        if self.vizFunctions:
            for f in self.vizFunctions:
                f( evalResults )
        return evalResults
    
if __name__ == "__main__":

    # example use case

    from simConfig import simConfig
    from collectors.randomCollectors import randomLinear
    
    # create MLSF instance, and specify 50% of training data to be used for evaluation.
    # also use config file simConfig
    mlsf = MLSF( simConfig, trainingRatio=0.50 )

    # evaluate MLSF after initial training. This is stored for later
    mlsf.eval()

    # send mlsf data from 'noPeer' labelled 'A'
    #mlsf.sendData( 'noPeer', [ 1.0, 1.0 ], 'A' )

    # Initialize randomCollector
    coll = randomLinear()

    # send 43 random samples to MLSF, from peer1
    for i in range(43):
        mlsf.sendData( 'peer1', coll.produceSample() )

    # evaluate MLSF again after samples have been sent. Likely some will have been trained on
    mlsf.eval()

    # Generate a report on each evaluation done, along with a short final report
    mlsf.report()

    log = mlsf.dataLog()

    #print log
