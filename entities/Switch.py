'''
Created on Feb 10, 2024

@author: mfontane
'''

from entities.Entities import Entities

class Switch(Entities):
    '''
    classdocs
    '''


    def __init__(self, bot, entityFilter, extendEntity, icon, statedict):
      super().__init__(bot, entityFilter, extendEntity, "switch", icon,  statedict)
