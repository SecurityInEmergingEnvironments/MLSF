'''
    Example/default configuration file for MLSF
'''

simConfig = {

    'Application':
    {
        'name': 'defaultApp',
        'params':
        {
            'debug': False,
            'bs:': 10,
            'features': None
        }
    },
    'Defense':
    {
        'name': 'defaultDefense',
        'params':
        {}
    },
    'Algorithm':
    {
        'name': 'SVM',
        'params':
        {
            #could use this to create basic training data
            #'trainingData': [[1.0, 2.0], [ 2.0, 3.0 ]],
            'gamma': 0.5,
            'c': 2.0
        }
    },
    'dataCollector':
    {
        'name': 'randomLinear',
        'params':
        {
            'featSize': 2
        }
    },
    'Peers' :
    []  

}
