'''
    load a component by _name attribute. 
    to automatically be able to load components
        - TODO: import custom here?
        - import modules here
'''

from applications.application import application
from defense.defense import defense
from MLAlgorithms.MLAlgorithm import MLAlgorithm
from collectors.randomCollectors import randomLinear
from custom import *

def loadComponent( name ):
    if name in lib.keys():
        return lib[ name ]
    return None

lib = {}

for elementKey, element in globals().items():
    # need better check for class here
    if type(element) == type:
        lib[ element._name ] = element
