#!/usr/bin/python2

'''
    example of targeted attack and results for old MLSF, and used in
    summer paper on incremental learning. This will not work."

'''

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from MLSF.MLSF import MLSF
from MLSF.applications import application
from MLSF.MLAlgorithms import *
from MLSF.cli import *
from MLSF.peers import peer
from MLSF.attacks import *
from MLSF.collectors import *
from time import sleep
import json

# How do we:
# 1) want to pass arguments into these modules
# 2) want to handle passing in proxy objects

#defenseArgs = { 'radius': 1.0 }
#dataSourceArgs = { 'fileName': 'basicTest' }

def variance( l ):
    return float( max(l) - min(l) )

def normalize( data ):
    results = []
    for testD in data:
        maxD = max( testD )
        print maxD
        minD = min( testD )
        denominator = maxD - minD
        newTestD = []
        for d in testD:
            newD = ( d - minD ) / denominator
            newTestD.append( newD )
        results.append( newTestD )
    return results

def numDiff( base, test ):
    count = 0
    for d1, d2 in zip( base, test ):
        if np.sign( d1 ) != np.sign( d2 ):
            count += 1
    return count

algArgs = { 'c' : 1.0, 'bs' : 1 }

dataSourceArgs = { 'fileName': 'parabolic.mat' }

mlsf = MLSF( remote=True, dataSource=matLabCollector, defense=defense, application=application, algorithm=MLAlgorithm, dcargs=dataSourceArgs, algArgs=algArgs )
#mlsf = MLSF( remote=True, dataSource=irisCollector, defense=riskDefense, application=application, algorithm=MLAlgorithm, dcargs=dataSourceArgs, dargs=defenseArgs )

xx, yy = np.meshgrid(np.linspace(0,4,400), np.linspace(0,4,400))

Deval = []
volList = []
misClassList = []
riskList = []


testNum = 1

algorithm=MLAlgorithm

for k in ['sgd']:#, 'linear', 'sgd' ]:
    
    if k == 'sgd':
        algorithm=onlineSVM
        mlsf.reset( algorithm=onlineSVM )
        algArgs[ 'alpha' ] = 0.0001
    algArgs[ 'kernel' ] = k
    
    #if k == 'rbf':
    #    dcArgs = { 'fileName': 'NaiveParabolicAttack' }
    #    dataSourceArgs = { 'fileName': 'parabolic.mat' }
    #else:
    dcArgs = { 'fileName': 'NaiveLinearAttack' }
    dataSourceArgs = { 'fileName': 'linear.mat' }
     
    # set batch size to 1 so we can test penalty parameter
    algArgs[ 'bs' ] = 1

    # test different values of penalty parameter
    for C in [ 0.1, 1.0, 10.0 ]:
        algArgs[ 'alpha' ] = C * .1
        
        misClassList.append([])
        volList.append([])
        riskList.append([])
        algArgs[ 'c' ] = C
        mlsf.reset( algArgs=algArgs, dcargs=dataSourceArgs )
        evalList = [ mlsf.Deval() ]
        # create an external peer and connect to the mlsf proxy object
        # save eval data on initial model
        Deval1 = mlsf.Deval()
        Acount = 0
    
        # save state of initial training data
        if k == 'sgd':
            mlsf.saveState( 'alpha = ' + str( algArgs[ 'alpha' ] ), testNumber=testNum, count=Acount )
        else:
            mlsf.saveState( 'C = ' + str( C ), testNumber=testNum )
    
        trainingData = mlsf.getTrainingData()
        testPeer = peer( mlsf=mlsf, name='targetedAttack', trainingData=trainingData, algorithm=algorithm,
                         dataCollector=targetedAttack, frequency=0, dcargs=dcArgs, algArgs=algArgs )
        
        # count is number of samples needed to take over point
        while testPeer.running:
            testPeer.step()
            risk = mlsf.getRisk()
            vol = mlsf.getVolatility()
            volList[testNum-1].append( vol )
            riskList[ testNum - 1 ].append( risk )
            evalList.append( mlsf.Deval() )
            misClassList[ testNum - 1 ].append( float( numDiff( evalList[ 0 ], evalList[ -1 ] ) ) )
            Acount += 1

        # save eval data after model is attacked

        if k == 'sgd':
            mlsf.saveState( 'alpha = ' + str( algArgs[ 'alpha' ] ), testNumber=testNum, count=Acount )
        else:
            mlsf.saveState( 'C = ' + str( C ), testNumber=testNum, count=Acount )
        
        Deval2 = mlsf.Deval()
        
        Deval.append([Deval1, Deval2])

        #if k == 'sgd':
        #    algArgs[ 'alpha' ] *= 100

        testNum += 1

    # set penalty parameter to 1 so we can test batch size
    algArgs[ 'c' ] = 1.0

    for bs in [ 1, 2, 3 ]:
        algArgs[ 'bs' ] = bs
        misClassList.append( [] )
        riskList.append([])
        volList.append([])
        mlsf.reset( algArgs=algArgs, dcargs=dataSourceArgs )
        evalList = [ mlsf.Deval() ]
        # create an external peer and connect to the mlsf proxy object

        # save eval data on initial model
        Deval1 = mlsf.Deval()
        Acount = 0
    
        # save state of initial training data
        mlsf.saveState( 'bs = ' + str( bs ), testNumber=testNum, count=Acount )
    
        trainingData = mlsf.getTrainingData()
        testPeer = peer( mlsf=mlsf, name='targetedAttack', trainingData=trainingData, algorithm=algorithm,
                         dataCollector=targetedAttack, frequency=0, dcargs=dcArgs, algArgs=algArgs )
        
        # count is number of samples needed to take over point
        while testPeer.running:
            testPeer.step()
            risk = mlsf.getRisk()
            vol = mlsf.getVolatility()
            volList[testNum-1].append( vol )
            riskList[ testNum - 1 ].append( risk )
            evalList.append( mlsf.Deval() )
            misClassList[ testNum - 1 ].append( float( numDiff( evalList[ 0 ], evalList[ -1 ] ) )  )
            Acount += 1

        # save eval data after model is attacked

        mlsf.saveState( 'bs = ' + str( bs ), testNumber=testNum, count=Acount )
        Deval2 = mlsf.Deval()
        Deval.append( [ Deval1, Deval2 ] )

        testNum += 1

# result: each kernel has 6 tests, with 3 columns and 2 rows.


flipSamp = []

for Dpair in Deval:
    misclassifications = numDiff( Dpair[0], Dpair[1] )
    percent = ( float( misclassifications ) / float( len( Dpair[ 0 ] ) ) ) * float( 100 )
    flipSamp.append( [ misclassifications, percent ] )
print flipSamp
mlsf.visualize( flipSamp )
axes=[]
print misClassList
misClassListNorm = normalize( misClassList )
print misClassListNorm
riskListNorm = normalize( riskList )
volListNorm = normalize( volList )
print volList, 'asdasdfadsf'
volListNorm[ 0 ] = [1.0, 0.0]
print volListNorm, 'adsfasdf'
for e, test in enumerate( zip( misClassListNorm, riskListNorm, volListNorm ) ):
    axes.append(plt.subplot( 6, 3, e+1 ))
    for axis in [ axes[ -1 ].xaxis, axes[ -1 ].yaxis ]:
        axis.set_major_locator( ticker.MaxNLocator(integer=True) )
    #print test[0]
    vVol = variance( volList[ e ] )
    vRisk = variance( riskList[ e ] )
    plt.plot( np.array( test[0] ), '--', label='Misclassification Percent on Deval' )
    #print np.array(test[1])*max( test[0] )
    plt.plot( np.array(test[1]), '-', label='Empirical Risk' )
    #print test[2]
    print test[2]
    print vol
    plt.plot( 1 - np.array( test[2] ), '-.', label='Stability' )
    plt.title( 'Stability Variance: %.2f Risk Variance: %.2f' % ( vVol, vRisk ) )
    if e == 0:
        plt.legend( bbox_to_anchor=(.75,1.25,2.,.102), loc=3, ncol=3, mode='expand', borderaxespad=0. )

    plt.ylabel( 'Normalized Metric' )
    plt.xlabel( 'Number of Samples Sent' )    
    #plt.xticks(())
    #plt.yticks(())
#for ax, l in zip( [ axes[3] ], [ 'SGD' ] ):
#    ax.text( -.75, 5, l, rotation=90, size=15)
plt.show()

# calls peer.start() on all peers that MLSF spins up.
# peer.start() begins data thread for eaech peer
# mlsf.run()

#dataLog = mlsf.dataLog()
#print 'all data since mlsf started running:'
#print '****************************'
#print json.dumps( dataLog, sort_keys=True, indent=4, separators=( ',', ': ' ))
#
## do stuff with dataLog
#
## query for testPeer data( our peer we define above)
## printing json output to show you what is actually stored right now
#testPeerData = mlsf.queryData( 'peer', 'testPeer' )
#print '\n\ntestPeer data:'
#print '****************************'
#print json.dumps( testPeerData, sort_keys=True, indent=4, separators=( ',', ': ' ))

def visualize( mlsf, erase=True ):
        num = 0
        mlsf.application.vis()
        for plotNum, state in enumerate( mlsf.states ):
                data = state[ 0 ]
                samples = []
                for entry in data:
                    samples.append( list( entry['sample'][0] ) )
                X_2d = []
                for sample in samples:
                    X_2d.append(sample[0])
                Y_2d = []
                for sample in samples:
                    Y_2d.append(sample[1])
                xx, yy = np.meshgrid(np.linspace(0,4,200), np.linspace(0,4,200))
                plt.subplot( 3, 3, plotNum + 1 )
                plt.title( "%d samples" % ( len( samples ) ) )
                Z = state[ 1 ]
                plt.pcolormesh( xx, yy, -Z, cmap=plt.cm.RdBu )
                #plt.scatter(X_2d, Y_2d, cmap=plt.cm.RdBu_r )
                plt.xticks(())
                plt.yticks(())
                plt.axis('tight')
                num = plotNum + 1

        data = mlsf.dataLog()
        samples = []
        for entry in data:
            samples.append( list( entry['sample'][0] ) )
        #X_2d = samples[:, :2]
        #print X_2d, 'adsfasdfasdf'
        X_2d = []
        for sample in samples:
            X_2d.append(sample[0])
        Y_2d = []
        for sample in samples:
            Y_2d.append(sample[1])
        xx, yy = np.meshgrid(np.linspace(0,4,200), np.linspace(0,4,200))
        plt.subplot( 3, 3, num + 1 )
        plt.title( "%d samples" % ( len( samples ) ) )
        Z = mlsf.application.algorithm.model.decision_function( np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        plt.pcolormesh( xx, yy, -Z, cmap=plt.cm.RdBu )
        #plt.scatter(X_2d, Y_2d, cmap=plt.cm.RdBu_r )
        plt.xticks(())
        plt.yticks(())
        plt.axis('tight')
        plt.show()
        print 'asdf'
        return 1

