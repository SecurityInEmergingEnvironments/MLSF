#This class will define the peer or source where a particular request is coming from.
#this class will have an attack method and a regular data generation model.
#parts of this class offer redundant access to information... Should be cleaned up.

from peer import peer
import cmd
from MLSF.simObject import restObject

class interactivePeer( peer, cmd.Cmd ):
    
    prompt = 'user $'

    def __init__( self, ip, port, *args, **kwargs  ):
        '''
        The peer class will have an attack module in order to generate the attack data that it sends.
        Will use default value replacement to create desired peer.
        '''
        '''The name of the peer will be used to identify the peers submission to the framework within '''
        
        #peer.__init__( self, *args, **kwargs )
        cmd.Cmd.__init__( self )
        self.mlsf = restObject( ip, port, *args, **kwargs )
    
    def returnSampleData(self, simRound=0):
        '''
        Send data to the framework application to be analyzed in the machine learning application.
        Uses the round number as a data stamp in the resources collection before sending to application.
        '''
        self.createNewSample()

        self.resources.append( ( str( round ), self.sampleToSend ) )
        return self.sampleToSend

    def do_sendSample( self, line ):
        '''
            sendSample [sample] [label]
        '''
        if not line:
            print 'no arguments given'
            self.do_help()
            return
        line = line.strip( ' ' )
        args = line.split()
        label = ''
        sample = args[ 0 ]
        label = args[ 1 ]
        sample = eval( sample )
        print self.mlsf.get( 'sendApp', peer='user', sample=sample, label=label )

    def do_predict( self, line ):
        '''
            predict [sample]
        '''
        if not line:
            print 'no arguments given'
            self.do_help()
            return
        line = line.strip( ' ' )
        args = line.split()
        sample = args[ 0 ]
        sample = eval( sample )
        print self.mlsf.get( 'predict', peer='user', sample=sample )
