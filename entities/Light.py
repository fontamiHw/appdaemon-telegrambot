'''
Created on Feb 10, 2024

@author: mfontane
'''

from entities.Entities import Entities

class Light(Entities):
    '''
    classdocs
    '''


    def __init__(self, bot, entityFilter, extendEntity, icon, statedict):
      super().__init__(bot, entityFilter, extendEntity, "light", icon,  statedict)  