"""
@author  Mateus Paiva Matiazzi
"""

import numpy as np

class ValueTable(object):

    table = None
    initValue = None

    def __init__(self, row, column):
        self.row = row
        self.column = column

    def initializeTable(self, initValue):
        self.initValue = initValue
        self.table = np.reshape([initValue]*self.column*self.row, (self.row, self.column))

    def returnTable(self):
        return self.table

    def printTable(self):
        print "Value Table:", self.table

    def updateTable(self, state, action, value):
        self.table[state][action] = value

    def returnState(self, state):
        return self.table[state]

    def stateValue(self, state, action):
        return self.table[state][action]

    def maxState(self, state):
        return max(self.table[state].tolist())

    def maxAction(self, line, possibleActions):
        tmp = self.table[line]
        aux = -100000.0 #-inf
        for i in possibleActions:
            if tmp[i+2] > aux:
                aux = tmp[i+2]
                act = i
        return act
