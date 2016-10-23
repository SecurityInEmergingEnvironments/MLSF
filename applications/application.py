'''
    AUTHORS: Cody Burkard, Julio Perez
    University of Washington, Bothell
    Security in Emerging Environments

    Application base class
    
    main API components for app:
        - TODO: initialize
        - predict
        - train
        - look?
        - extractFeatures
        - defense

'''
from evaluation import Accuracy

class application(object):
    
    _name = 'defaultApp'
    description = 'Application -> Base application class'

    def __init__( self, evalMethods=[], debug=False, bs=10,
                  algorithm=None, trainingData=[], defense=None,
                  defArgs={}, algArgs={}, *args, **kwargs ):

        self.debug=debug
        self.workingSamples = {}
        self.newSamples = []
        self.sampleIDs = []
        self.bs = bs

        # TODO: create way to set analysis methods
        # Accuracy is always an eval method by default
        self.analysisMethods = list( set( [ Accuracy ] + evalMethods ) )

        for method in evalMethods:
            self.analysisMethods.append( method )

        self.trainingData = trainingData

        self.algorithm = algorithm( **algArgs ) if algorithm else None

        self.defense = defense( **defArgs ) if defense else None
        
        if trainingData:
            self.defense.setup( trainingData=trainingData, algorithm=self.algorithm )
            self.algorithm.setup( trainingData )

    def reset( self, trainingData=None, algorithm=None, dargs={}, algArgs={} ):
        print 'havent implemented reset yet!\n'
        pass

    def newSample( self, sample, classification, sampleID ):
        self.newSamples.append( [ sample, classification ] )
        self.sampleIDs.append( sampleID )
        IDs = []
        if len( self.newSamples ) == self.bs:
            self.algorithm.train( self.newSamples )
        
            IDs = self.sampleIDs
            self.newSamples = []
            self.sampleIDs = []
        return IDs

    # evaluate current model based on application's analysis methods.
    # results are returned as dictionart of methodName: result
    def eval( self, Deval=None, train=False, evalCallbacks=[] ):
        evalCallbacks += self.analysisMethods
        evalResults={}

        for evalFunction in evalCallbacks:
            # TODO: Maybe we can check here to see if my eval function
            # is compatible with alg?
            evalResults[ evalFunction.__name__ ] = evalFunction( Deval, self.algorithm )

        return evalResults

    def extractFeatures( self, sample ):
        '''
            called when a sample is received.
            returns a list of feature values
        '''
        return sample

    # Do NOT overwrite
    def send( self, peer, sampleID, sample, label=None, feedback=True ):
        '''
            metrics are all taken before training occurs on a sample,
            at same time as defense looks at it

            workingSamples are the samples that are currently being evaluated by
            the application for training. When returned to 
        '''

        sample = self.extractFeatures( sample )
        
        self.workingSamples = {}
        self.workingSamples[ sampleID ] = {}
        classification, dec_f = self.predict( peer, sample, df=True )
        self.workingSamples[ sampleID ][ 'dec_f_beforeTrain' ] = dec_f

        # could add in risk associated with sample here
        self.workingSamples[ sampleID ][ 'classPrediction' ] = classification

        metricVals = {}
        if self.defense:
            # defense.metric()? maintain a list of metrics in defense that
            # it needs to use for defense to work
            if self.defense.metrics:
                for metric in self.defense.metrics:
                    val = metric( self.algorithm )
                    self.workingSamples[ sampleID ][ metric.__name__ ] = val
                    metricVals[ metric.__name__ ] = val

            # get defense feedback here
            accepted, defResults = self.defense.test( sample, peer,
                                         classification, metricVals )
            self.workingSamples[ sampleID ][ 'defResponse' ] = accepted
            self.workingSamples[ sampleID ][ 'trueLabel' ] = classification
            self.workingSamples[ sampleID ][ 'defFeedback' ] = defResults

            if accepted:
                # trainedSampleIds is the samples that were trained after adding
                # this new training sample
                trainedSampleIds = self.newSample( sample,
                                         classification, sampleID )
        else:
            accepted = True
            trainedSampleIds = self.newSample( sample, 
                                         classification, sampleID )

        for ID in trainedSampleIds:
            if ID not in self.workingSamples.keys():
                self.workingSamples[ ID ] = {}

            self.workingSamples[ ID ][ 'trained' ] = True
            self.workingSamples[ ID ][ 'trainRound' ] = sampleID

        if feedback:
            return self.workingSamples, classification
        else:
            return self.workingSamples, None

    # TODO: not yet implemented
    def look( self ):
        '''
            application specific 'peek'
            if peers should be able to look at the state of an application
            in any way, this function should return that data
        '''
        pass

    def predict( self, peer, sample, df=False ):
        '''
           Predict the label of sample
           sample: raw sample data
           returns ( extracted sample, predicted label )
           all other attributes are temporary for debugging
        '''
        if df:
            dec_f = self.algorithm.decision( sample )
        if self.debug: print "predicting label of %s" % str( sample )
        classification = self.algorithm.classify( sample )
        if self.debug: print 'classified as: ', classification

        if df:
            return classification, dec_f
        else:
            return classification 

    def __repr__( self ):
        "return name and description of this module"
        return self._name + self.description
