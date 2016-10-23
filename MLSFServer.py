#!/usr/bin/python2
'''
    AUTHORS: Cody Burkard, Julio Perez
    University of Washington, Bothell
    Security in Emerging Environments

    Simple MLSF server class. This object keeps track of local MLSF
    instances, and will allow connections to it
'''


import serpent
import uuid
import sys
from logging import *
from util import *
from MLSF import MLSF
from multiprocessing import Process, Pipe
import falcon
import json
#from peers import *
import Pyro4
import threading
from collectors.randomCollectors import *

class MLSFDaemon( object ):

    def __init__( self, ns=None, *argsv, **kwargs ):
        '''
           Create a test for a machine learning algorithm or a
           simulation of a machine learning attack
        '''
        
        # need to look through all components and map them here
        # genComponentMapping?
        self.MLSFObjects = {}
                
        # create a REST api object and add routes
        self.api = falcon.API()
        self.api.add_route( '/{command}',  self )
        self.api.add_route( '/objects/{object}', self )

    @Pyro4.expose
    def newSim( self, name, **mlsfArgs ):
        if name in self.MLSFObjects.keys():
            name += '2'
        while name in self.MLSFObjects.keys():
            name = name[ 0:-1 ] + str( int( name[ -1 ] ) +1 )
        sim = MLSF( **mlsfArgs )
        uri = self._pyroDaemon.register(sim, objectId=name)
        self.MLSFObjects[ name ] = uri
        return name, sim

    @Pyro4.expose
    def listSims( self ):
        retString = ''
        for name, uri in self.MLSFObjects.items():
            retString += name + ': ' + str( uri ) + '\r\n'
        return retString

    @Pyro4.expose
    def deleteSim( self, name ):
        if name in self.MLSFObjects.keys():
            self._pyroDaemon.unregister( name )
            self.MLSFObjects[ name ].exit()
            self.MLSFObjects.pop( name )
            return 1
        else:
            print 'No object named %s' %name
            return 0
    
    @Pyro4.expose
    def connect( self, name ):
        return self._pyroDaemon.objectsById[ name ]
        

    #TODO: implement REST API on top of the pyro api. Just serves pyro objects and URIs
    #def on_get( self, req, resp, command=None, object=None, *args, **kwargs ):
    #    '''
    #       Called when a get request is received
    #       req: Falcon request object
    #       resp: falcon http response
    #       command: command we would like to run on server
    #       object: if command is 'object', we dump JSON of object specified
    #    '''
    #    # Check to see if command is a class method. If so, execute it with
    #    # keyword arguments passed in with request
    #    if command:
    #        classMembers = inspect.getmembers( self,
    #                                predicate=inspect.ismethod )
    #        for methodMap in classMembers:
    #            if command in methodMap:
    #                resp.body = json.dumps( methodMap[ 1 ]( **req.params ) )
    #                resp.status = falcon.HTTP_200
    #    # If this is an object query, dump the JSON of the object in response
    #    if object:
    #        resp.body=json.dumps( self.objects, sort_keys=True,
    #                              indent=4, separators=( ',', ': ' ) )
    #        resp.status = falcon.HTTP_200

    #def on_post( self, req, resp, command, *args, **kwargs ):
    #    "Handle all POST requests"
    #    if command in self.commandMapping.keys():
    #        result = json.dumps( self.commandMapping[ command ]( **req.params ) )
    #        resp.body = result
    #        resp.status = falcon.HTTP_200
        

# start a Pyro4 Name Server
def startNS():
        Pyro4.naming.startNSloop()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument( 'ip', type=str, default=None, help='Local IP address to listen on' )
    parser.add_argument( '--port', type=int, default=0, help='Port to listen on' )
    args = parser.parse_args()
    ip = args.ip
    port = args.port

    daemon=Pyro4.Daemon( host=ip, port=port )
    server=MLSFDaemon()
    uri=daemon.register(server)
    nsThread=threading.Thread( target=startNS )
    nsThread.daemon = True
    nsThread.start()
    ns=Pyro4.locateNS()
    ns.register( "mlsfDaemon", uri )
    daemon.requestLoop() 
