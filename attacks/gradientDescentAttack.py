'''
    WARNING: This will not work
    TODO: fix this
'''

from MLSF.collectors import dataCollector
from MLSF.MLAlgorithms import MLAlgorithm
import numpy as np

class gradientDescent( dataCollector ):

    def __init__( self, trainingData, *args, **kwargs ):
        self.trainingData = trainingData
        self.algorithm = MLAlgorithm()
        self.algorithm.setup( trainingData = trainingData )
        self.b = self.algorithm.model.intercept_
        self.w = self.algorithm.model.coef_
        #self.a = -w[0] / w[1]
        self.xx = np.linspace( 0, 4 )
        #self.y = self.a * self.xx - (self.algorithm.model.intercept_[0] ) / w[1]
        self.gradient = None
        dataCollector.__init__( self, *args, **kwargs )
        totalGradient = 0
        loss, grad = self.hinge_loss( self.w, zip(*trainingData)[1], zip(*trainingData)[ 0 ]  )
        print loss, grad
        print 'dir: ', grad/np.linalg.norm(grad)

        print 'maxing out risk'
        print self.b
        print self.w
        print np.dot( self.w, [ 2, 2] ) - self.b
        #for label, sample in trainingData:
        #    print 'loss before gradient: ', np.dot(self.w, sample) + self.b
        #    grad = np.gradient( np.dot( self.w, sample ) + self.b )
        #    print 'gradient: ', grad
        #    totalgradient += grad
        #print totalGradient, 'totalgradient'
        #self.gradient = totalGradient

    def hinge_loss( self, w, x, y ):
        x = np.vstack(np.array(x))
        y = np.array(y)
        loss,grad = 0,0
        for (x_,y_) in zip(x,y):
            print y_, w, x_
            v = y_*np.dot(w,x_)
            print v
            loss += max(0,1-v)
            grad += 0 if v > 1 else -y_*x_
        return (loss,grad)

    def updateGradient( self, x, y, w, step ):
        grad = np.inf
        ws = np.zeros((2,0))
        ws = np.hstack((ws,w.reshape(2,1)))
        step_num = 1
        delta = np.inf
        loss0 = np.inf
        while np.abs(delta)>thresh:
            loss,grad = hinge_loss(w,x,y)
            delta = loss0-loss
            loss0 = loss
            grad_dir = grad/np.linalg.norm(grad)
            w = w-step*grad_dir/step_num
            ws = np.hstack((ws,w.reshape((2,1))))
            step_num += 1
        return np.sum(ws,1)/np.size(ws,1)
        #print self.xx
        #f = np.dot( self.w, self.xx ) + self.b
        #print self.w
        #print self.b
        #self.gradient = np.gradient( f )
        #print self.gradient
