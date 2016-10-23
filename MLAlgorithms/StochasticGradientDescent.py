'''
    WARNING: this will not currently work.
    TODO: fix this. 
'''

from MLAlgorithm.MLAlgorithm import MLAlgorithm
from sklearn.externals import joblib
from sklearn.linear_model import SGDClassifier
from sklearn.kernel_approximation import RBFSampler
import numpy as np

class onlineSVM( MLAlgorithm ):
    
    def __init__( self, *args, **kwargs ):
        # data will contain a list of dicts, each dict with a mapping of feature to value
        MLAlgorithm.__init__( self, *args, **kwargs )
        self.allClasses = []
        self.model = SGDClassifier( loss='hinge', penalty='l2', n_jobs=-1 )
        self.class1 = []
        self.class2 = []
        # we transform a feature set into this kernel classification using
        # self.transformation.fit_transform( Samples )
        self.transformation = RBFSampler( gamma=1, random_state=1 )

    def setup( self, trainingData, c=1.0, kernel='linear', bs=1, alpha=0.0001 ):
        '''set up the basic parts of the algorithm. What type of data do we need to store?'''
        self.samples = []
        self.labels = []
        self.bs = bs
        self.model = SGDClassifier( loss='hinge', penalty='l2', n_jobs=-1, shuffle=False, alpha=alpha )
        for sample in trainingData:
            self.samples.append( sample[ 1 ] )
            if sample[ 0 ] == -1:
                self.class1.append( sample[1] )
            elif sample[ 0 ] == 1:
                self.class2.append( sample[1] )
            self.labels.append( sample[ 0 ] )
        # make the labels list unique by casting to a set
        self.allClasses = list( set( self.labels ) )
        #self.model.partial_fit( np.array( self.transformation.fit_transform( self.samples ) ), np.array( self.labels ), classes=self.allClasses )
        self.model.partial_fit( np.array( self.samples ) , np.array( self.labels ), classes=self.allClasses )

    def train( self, sample, label, retrain=False ):
        '''Send data to algorithm and train on that data.'''
        if self.bs > 1:
            print 'batch training'
            return self.batchTrain( sample, label )
        self.samples.append( sample )
        self.labels.append( label )
        sample = np.array( sample )
        #sample = self.transformation.fit_transform( sample.reshape( 1, -1 ) )
        if retrain:
            self.model.partial_fit( np.array( self.samples ) , np.array( self.labels ), classes=self.allClasses )
            #self.model.partial_fit( np.array( self.transformation.fit_transform( self.samples ) ), np.array( self.labels ), classes=self.allClasses )
        else:
            print 'running partial fit on ', sample, label
            self.model.partial_fit( sample.reshape(1,-1), [ label ] )
            

    # not relevant for now
    def batchTrain( self, sample, label, *args, **kwargs ):
        '''Train on a list of data'''
        samples = []
        labels = []
        self.batch.append( [ sample, label ] )
        if len( self.batch ) == self.bs:
            for sample, label in self.batch:
                samples.append(sample)
                labels.append(label)
            self.model.partial_fit( np.array( samples ), np.array(labels) )
            self.batch = []

    def classify( self, data ):
        '''determine where the data falls. Depends on application.
           possible results could be good/bad data(ids), author, etc.'''
        data = np.array( data ).reshape(1,-1)
        #data = self.transformation.fit_transform( data.reshape(1, -1 ) )
        classification = self.model.predict( data )
        return classification[0]

