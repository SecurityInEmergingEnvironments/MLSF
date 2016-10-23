'''
    Evaluation Metrics to be used by eval() call
    All evaluation metrics should take parameters ( data, model )
'''
def Accuracy( data, algorithm ):
    #precision of just the evaluation data
    correct=0.0
    incorrect=0.0
    totalEval=float( len( data ) )
    for sample in data:
        classPrediction = algorithm.classify( sample[ 1:2 ] )
        trueLabel = sample[ 0 ]
        if trueLabel == classPrediction:
            correct += 1
        elif trueLabel != classPrediction:
                incorrect += 1
    if totalEval > 0:
        accuracy = float( correct / totalEval )
    else:
        accuracy = '?'
    return accuracy

