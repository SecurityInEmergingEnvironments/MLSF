#This class will define the peer or source where a particular request is coming from.
#this class will have an attack method and a regular data generation model.
from peer import peer

class basicPeer( peer ):
    
    description = 'basic Peer subclass for testing'

    def __init__( self, *args, **kwargs ):
        return peer.__init__( self, *args, **kwargs )

    def __str__( self ):
        return self.description

    def __repr__( self ):
        return self.description
