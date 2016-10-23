'''
    AUTHORS: Cody Burkard, Julio Perez
    University of Washington, Bothell
    Security in Emerging Environments

    MLSF data structure. Holds all important information in the simulation
    about the data being used

    The purpose of these classes is to handle data as it is passed through
    the framework.

    The basic useful ability of this class is to return data in different
    formats, with different data structures. This allows easy manipulation
    of this data, despite the complex nature of the data that is held.
'''

# TODO: We need to track what features are applied to a data entry,
#       and what the value of those features is calculated to be.

class entry( object ):

    def __init__( self, EID, sample, peer=None,
                  trainingData=False, trueLabel=None,
                  raw=True, *args, **kwargs ):
        '''
           Structure holding the information of a single data sample.
           sample: raw sample data sent to app
           peer: peer the sample came from of None if training
           phase: 1 if training, 2 if online
           malicious: whether sample is meant to be malicious( from peer )
           expectedLabel: label the peer is expecting sample to be classified
        '''
        self.entryNumber = EID
        self.peer = peer 
        # What was the defenses reaction?
        self.classPrediction = None
        # actual raw data to be sent to app
        self.sample = sample
        # extracted feature mapping of sample
        self.extractedSample = None
        # has this data been sent to the application?
        self.sent = True
        # has the application trained on this data?
        self.trained = False
        # The label that the sample was actual trained/predicted as
        self.trueLabel = trueLabel
        self.trainingData=trainingData
        self.defResponse=None

    def log( self, **kwargs ):
        for kwarg in kwargs.keys():
            if kwarg in self.__dict__:
                self.__dict__[ kwarg ] = kwargs[ kwarg ]
            else:
                #create new item
                self.__dict__[ kwarg ] = kwargs[ kwarg ]

    def raw( self ):
        "Serialize data into dict to be dumped to JSON"
        serializeable = {}
        for property, val in vars( self ).iteritems():
            serializeable[property] = val
        return serializeable

class data( object ):

    def __init__( self ):
        "data structure to hold all entries, and to be queried"
        self._results = {}
        self.sampleNumber = 0
        self.entries = {}
        self.lastEntry = None

    # Store the results of the evaluation in a dict, mapped from the number of samples sent
    def saveEval( self, Eresults ):
        self._results[ self.sampleNumber ] = Eresults

    def genReport( self ):
        results = {}
        results[ 'total number of samples' ] = len( self.entries )
        for _, entry in self.entries.items():
            if entry.trueLabel:
                if entry.trueLabel in results.keys():
                    results[ entry.trueLabel ] += 1
                else:
                    results[ entry.trueLabel ] = 0
        return results

    def getResults( self ):
        return self._results

    def setTrainingData( self, trainingData, labelled=True ):
        self.trainingData = trainingData # ?
        for sample in trainingData:
            if labelled:
                label = sample[ 0 ]
            self.newEntry( sample=sample[ 1 ], trueLabel=label, trainingData=True, raw=True, trained=True )

    def newEntry( self, *args, **kwargs ):
        '''
           Create a new application data entry
           returns entry ID number
        '''
        self.entries[ self.sampleNumber ] = entry( self.sampleNumber, *args, **kwargs )
        self.lastEntry = self.entries[ self.sampleNumber ]
        self.sampleNumber += 1
        return ( self.sampleNumber - 1 )

    def log( self, EID, *args, **kwargs ):
        self.entries[ EID ].log( **kwargs )

    def rawData( self, phase=None ):
        '''
           get a list of all data sent to the framework
           phase: Only query for data in a specific phase
           Returns a list of raw data entries.
        '''
        data = []
        for _, entry in self.entries.items():
            data.append( entry.raw() )
        return data
    
    def query( self, **attrDict ):
        '''
           Query our data object for all objects with certain attributes

               Example: "query( sent=True )"
               returns all samples that have been sent to the application

           returns all entries with attributes specified
        '''
        data = []
        for attr, val in attrDict.items():
            for _, entry in self.entries.items():
                if attr in vars( entry ):
                    if val:
                        if str( vars( entry )[ attr ] ) == str( val ):
                            data.append( entry.raw() )
        return data

    def peerMap( self ):
        "Returns a dict of peers mapped to a list of their data"
        peerData = {}
        for entry in self.entries:
            if entry.peer not in peerData:
                peerData[ entry.peer ] = []
            peerData[ entry.peer ].append( entry.sample )
        return peerData

