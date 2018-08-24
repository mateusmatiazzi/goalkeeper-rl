"""
@author  Mateus Paiva Matiazzi
"""

import random as rd

class GreedyExplorer(object):

    def __init__(self, goalEnvironment, valueTable, epsilon=0.3, decay=1, minEpsilon=0.01):
        self.epsilon = epsilon
        self.decay = decay
        self.env = goalEnvironment
        self.table = valueTable
        self.minEpsilon = minEpsilon

    def updateEpsilon(self, ep):
        self.epsilon = ep

    def updateDecay(self, decay):
        self.decay = decay

    def useDecay(self):
        if self.epsilon > self.minEpsilon:
            self.epsilon *= self.decay

    def chooseAction(self):
        listActions = self.env.listOfActions()
        #state is a list from valueTable
        if rd.random() < self.epsilon:
            act = rd.choice(listActions)
        else:
            # action with max value
            act = self.table.maxAction(self.env.returnState(), listActions)
        return act