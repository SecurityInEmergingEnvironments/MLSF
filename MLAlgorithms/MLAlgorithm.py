#NOTE: maybe we want a "data" data structure that we can use to store data and features?
# NOTE: problem with SKLEARN's svm: we cannot dynamically add training data. we must
#       retrain the entire model if we would like to add training data.

from sklearn.neighbors import RadiusNeighborsClassifier as rnc
from sklearn.metrics import hinge_loss
from sklearn.preprocessing import scale
from sklearn.externals import joblib
from sklearn.svm import SVC
import numpy as np

class MLAlgorithm( object ):
    
    _name = 'SVM'

    def __init__( self, trainingData=[], c=1.0, kernel='rbf', gamma=1.0, debug=False, *args, **kwargs ):

        self.debug=debug
        self.samples = []
        self.labels = []

        # Model variables
        self.c=1.0 # penalty parameter
        self.gamma=gamma # gamma for RBF Kernel
        self.model = SVC( C=self.c, kernel=str(kernel), gamma=gamma )

        # state variables
        self.fitted=False

        if self.debug: print self.model

        if trainingData:
            for sample in trainingData:
                self.samples.append( sample[ 1 ] )
                self.labels.append( sample[ 0 ] )
            self.model.fit( np.array( self.samples ), np.array( self.labels ) )
            self.fitted=True
        else:
            print 'WARNING: no training data sent to algorithm. Model is not fit\n'

    def train( self, newTrainingData,  *args, **kwargs ):
        '''Send data to algorithm and train on that data.'''
        for sample, label in newTrainingData:
            self.samples.append( sample )
            self.labels.append( label )
        if self.debug: print 'FITTING new data:', newTrainingData
        self.model.fit( np.array( self.samples ), np.array( self.labels ) )
        self.fitted=True

    def classify( self, data ):
        '''determine where the data falls. Depends on application.
           possible results could be good/bad data(ids), author, etc.'''
        
        if not self.fitted:
            print 'ERROR: Attempting to classify data before model has been trained\n'
            return 0
        
        # if data is just a feature list, turn it into a list of lists
        # ( This is what sklearn uses, and it needs to be reshaped )
        if type( data[0] != list ):
            data = [ data ]

        # if predicting length of single sample, reshape data for sklearn
        if len( data ) == 1:
            data = np.array(data).reshape( 1, -1 )

        classification = self.model.predict( data )
        return classification[0]

    def decision( self, data ):
        '''determine where the data falls. Depends on application.
           possible results could be good/bad data(ids), author, etc.'''
        
        if not self.fitted:
            print 'ERROR: Attempting to classify data before model has been trained\n'
            return 0
        
        if type( data[0] != list ):
            data = [ data ]

        if len( data ) == 1:
            data = np.array(data).reshape( 1, -1 )

        dec = self.model.decision_function( data )
        return dec
