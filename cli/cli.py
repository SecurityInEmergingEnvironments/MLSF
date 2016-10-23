'''
    AUTHORS: Cody Burkard, Julio Perez
    University of Washington, Bothell
    Security in Emerging Environments

    A command line interface for the MLSF framework. Aims to provide
    useful functionality for a user to quickly run tests on an
    application and interpret the results.
'''

import cmd
from simConfig import *

class MLSF_cli( cmd.Cmd ):

    prompt = 'MLSF $ '

    def __init__( self, mlsfServer ):
        cmd.Cmd.__init__( self ) 
        self.mlsfServer = mlsfServer

    def do_listSims( self, line ):
        print self.mlsfServer.listSims()
        return

    def do_createSim( self, line ):
        args = self.parse( line )[1]
        name = args[0]
        simConfig=eval(args[ 1 ])
        trainingRatio = float( args[2] )
        self.mlsfServer.newSim( name, config=simConfig, trainingRatio=trainingRatio )

    def do_deleteSim( self, line ):
        args = self.parse( line )[ 1 ]
        simName = args[ 0 ]
        success = self.mlsfServer.deleteSim( name=simName )
        if success:
            print 'successfully deleted %s' % simName
        else:
            print 'could not delete %s' % simName

    def parse( self, line, minArgLen=None, maxArgLen=None ):
        '''
           Executes error handling on the incoming line and parses it into a list
        '''
        if not line:
            info( 'No arguments given.\n' )
            self.do_help()
            return 0
        args = line.split()
        if minArgLen:
            if len( args ) < minArgLen:
                warning( 'Too few args\n' )
                return 0
        if maxArgLen:
            if len( args ) > maxArgLen:
                warning( 'Too many args\n' )
                return 0
        return len( args ), args
        
    
    def emptyline( self ):
        "Overwritten so that last command is not repeated"
        pass

    # should allow us to send command to specific MLSF instance
    def default( self, line ):
        "When an invalid command is entered, print error and help"
        print 'Command not recognized: %s' % line
        self.do_help( None )

    def do_printLog( self, line ):
        print self.mlsf.dataLog()


    def cmdloop( self ):
        '''Overwritten to catch keyboard interrupts'''
        try:
            cmd.Cmd.cmdloop( self )
        except KeyboardInterrupt:
            info( '\ncaught ctrl-c. exiting cli\n' )
            print
            return

# connect to a running MLSF server and start up a cli on the server
if __name__ == '__main__':
    
    import Pyro4
    mlsfServer = Pyro4.Proxy( "PYRONAME:mlsfDaemon" )
    cli = MLSF_cli( mlsfServer )
    cli.cmdloop()
