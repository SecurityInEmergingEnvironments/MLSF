'''
    AUTHORS: Cody Burkard, Julio Perez
    University of Washington, Bothell
    Security in Emerging Environments

    Base Defense class

    Always returns True on test.
'''

class defense( object ):

    _name="defaultDefense"
    description="defense -> Base defense mechanism class"

    def __init__( self, peers=None, data=None, *args, **kwargs ):
        '''
           base defense class
           peers: peers that are known at the start( do we want this? )
           data: known data at the start( may not use this )
        '''
        self.peers = peers
        self.dataLog = data
        self.metrics = [] # metrics that the defense requires. Methods
        # Ex. self.metrics = [ accuracy, hing_loss, Empirical_Risk ] where each are methods

    def test( self, sample, peer=None, label=None, metrics=[] ):
        '''
           Determine whether or not to accept data. Override this.
           returns True, defenseResults
           ( any results from defense that may be helpful in later analysis )
        '''
        return True, {}


    # maybe we dont need this?
    def testTrainingData( self, data ):
        '''
           analyze training data
           return list of good data after analysis
        '''
        return data

    def setup( self, trainingData=None, *args, **kwargs ):
        '''
           Initialize all elements of a defense module. Override this.
           trainingData: list of any intial data used by defense algorithm
        '''
        pass

    def reset( self ):
        pass

    def __repr__( self ):
        "return description of this defense class"
        return self.description
