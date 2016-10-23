import os
#from MLSF.core import component
class dataCollector( object ):

    def __init__( self, debug=False, *args, **kwargs ):
        "data collection mechanism for training"
        self.data = []
        self.debug=debug

    #TODO: if we collect a second time, and want more samples, what do we do?
    def collectTrainingData( self, numSamples=100 ):
        '''collect all of the data from our specified file for training'''
        # If we have already collected training data, do not collect again
        if self.data:
            return self.data
        data = []
        for i in range( numSamples ):
            data.append( self.produceSample( label=True ) )
        #with open( self.path, 'r' ) as f:
        #    for sample in f:
        #        data.append( eval(sample) )
        self.data = data
        return data

    def addData( self, label, data ):
        '''Method to collect data and store in dictionary. Should be
           called by "collect" method'''
        self.data[ label ] = data

    def produceSample( self, restart=True ):
        '''
           return data from file line by line every time this function is called
           currently a huge security risk because of 'eval'
        '''
        try:
            sample = eval( self.f.readline() )
        except SyntaxError:
            if restart:
                print 'all contents of file read. Reading from beginning again'
                self.f = open( self.path, 'r' )
                sample = eval( self.f.readline() )
            else:
                print 'end of file, no more samples'
                return None
        return sample

    def toJSON( self ):
        "send data to JSON object"
        pass

    def send( self, server ):
        '''This is for remote server capabilities. send data to
           simulation server with pyro'''
        pass

    def store( self ):
        '''store data as a set of files in rootDir'''
        pass
