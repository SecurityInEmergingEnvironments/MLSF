import os
from dataCollector import dataCollector
from MLSF.util.util import importMatlabData

class matLabCollector( dataCollector ):

    def __init__( self, rootDir=None, path='', fileName='parabolic.mat', *args, **kwargs ):
        "data collection mechanism for training"
        #self.data = {}
        #self.rootDir = rootDir
        #if path:
        #    self.path=path
        #else:
        #    self.path = os.getcwd() + '/MLSF/trainingData/' + fileName
        dataCollector.__init__( self )
        self.dataList = importMatlabData( self.rootDir + fileName )

    def setFileName( self, fileName='parabolic.mat', *args, **kwargs ):
        self.dataList = importMatlabData( self.rootDir + fileName )


    def collectTrainingData( self ):
        '''collect all of the data from our specified file for training'''
        data = []
        #with open( self.path, 'r' ) as f:
        #    for sample in f:
        #        data.append( eval(sample) )
        data = self.dataList
        return data

    def addData( self, label, data ):
        '''Method to collect data and store in dictionary. Should be
           called by "collect" method'''
        self.data[ label ] = data

    def produceSample( self ):
        '''
           return data from file line by line every time this function is called
           currently a huge security risk because of 'eval'
        '''
        #try:
        #    sample = eval( self.f.readline() )
        #except SyntaxError:
        #    print 'all contents of file read. Reading from beginning again'
        #    self.f = open( self.path, 'r' )
        #    sample = eval( self.f.readline() )
        #return sample
        print 'no samples to give'
        pass

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
