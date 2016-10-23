import datetime
import time
import scipy.io as sio

def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp( ts ).strftime( '%H:%M:%S:%f' )
    return st

def inheritors( klass ):
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses

def importMatlabData( fileName ):
    try:
        matContents = sio.loadmat( fileName )
    except Exception as msg:
        print 'ERROR importing matlab content: ', msg
        return 0
    # data is stored as a numpy array of numpy arrays
    # convert to list for our use
    matData = list( matContents[ 'data' ] )
    data = []
    for sample in matData:
        data.append( [ sample[ 2 ], [ sample[ 0 ], sample[ 1 ] ] ] )
    return data

def sign( x ):
    "Returns the sign of a number x"
    if x > 0: return 1
    elif x < 0: return -1
    elif x == 0: return 0
    else: return x
