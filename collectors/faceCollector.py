'''
    WARNING: this will not work
    TODO: fix this
'''

import os
import numpy as np
from dataCollector import dataCollector
from sklearn import datasets
from sklearn.datasets import fetch_lfw_people
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# NOTE: requires internet access

class irisCollector( dataCollector ):

    def __init__( self, *args, **kwargs ):
        "data collection mechanism for training"
        dataCollector.__init__( self )
        self.dataList = []

    # used to be for faces
    # there are only 236 images of two different people.
    # This is best num I can get
    def collectTrainingData( self ):
        '''collect all of the data from our specified file for training'''
        #people = fetch_lfw_people( min_faces_per_person=236, resize=.4 )
        #nsamples, h, w = people.images.shape
        #
        ## labels
        #y = people.target
        #X = people.data
        #n_features = X.shape[1]

        #tNames = people.target_names
        #n_classes = tNames.shape[0]


        #samples, labels = self.extractTwoPeople( X, y, rand=False )

        #samples = [ [1.1, 2.2, 3.3, 4.4], [ 2.2, 3.3, 6.2, 7.2 ], [ 6.2, 8.3, 2.9, 3.8 ] ]
        #labels = [ 0, 1, 2 ]

        iris = datasets.load_iris()
        samples = iris.data[ 0:100 ]
        labels = iris.target[ 0:100 ]


        # run pca to find best two features
        lda = LinearDiscriminantAnalysis( )
        lda.fit( samples, labels )
        scalings = lda.scalings_
        f1 = list( scalings ).index( min( scalings ) )
        f2 = list( scalings ).index( max( scalings ) )
        X = []
        for sample in samples:
            X.append( [ float( sample[ f1 ] ), float( sample[ f2 ] ) ] )
        y = []
        for label in list( labels ):
            if label == 0:
                label = -1
            y.append( int( label )  )

        #print zip(y, X)
        self.dataList = zip( y, X )
        return self.dataList

    # defaults to extracting first two people in target_names
    def extractTwoPeople( self, samples, labels, rand=False ):
        p1indices = np.where( labels == 0 )[ 0 ]
        p2indices = np.where( labels == 1 )[ 0 ]
        newSamples = []
        newLabels = []
        for i in p1indices:
            newSamples.append( samples[ i ] )
            newLabels.append( labels[ i ] )
        for i in p2indices:
            newSamples.append( samples[ i ] )
            newLabels.append( labels[ i ] )
        return newSamples, newLabels

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

