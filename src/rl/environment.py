"""
@author  Mateus Paiva Matiazzi
"""

from random import randint

class Environment(object):

    def __init__(self, arenaStates, numberActions=5):
        self.arenaStates = arenaStates
        self.numberActions = numberActions
        self.ballPos = None
        self.keeperPos = None
        self.reset()

    def _numberActions(self):
        return self.numberActions

    def _numberStates(self):
        return self.arenaStates**2

    def _keeperPos(self):
        return self.keeperPos

    def _ballPos(self):
        return self.ballPos

    def setBallPos(self, num):
        self.ballPos = num

    def setKeeperPos(self, num):
        self.keeperPos = num

    def randomKeeper(self):
        self.setKeeperPos(randint(0,self.arenaStates-1))

    def randomBall(self):
        self.setBallPos(randint(0,self.arenaStates-1))

    def reset(self):
        self.ballPos = 0
        self.keeperPos = 0

    def listOfActions(self):
        if self.keeperPos == 11:
            return [-2, -1, 0]
        elif self.keeperPos == 10:
            return [-2, -1, 0, 1]
        elif self.keeperPos == 0:
            return [0, 1, 2]
        elif self.keeperPos == 1:
            return [-1, 0, 1, 2]
        else:
            return [-2, -1, 0, 1, 2]

    def getReward(self):
        reward = -1
        if self.isGoal():
            reward = 100
        return reward

    def returnState(self):
        return self.arenaStates*self.ballPos + self.keeperPos

    def _moveInDir(self, pos, direction):
        return pos + direction

    def performAction(self, action):
        tmp = self._moveInDir(self.keeperPos, action)
        # print "Action choosen: ", action, " keeperState: ", self.keeperPos, "ballPos", self.ballPos
        self.keeperPos = tmp

    def isGoal(self):
        if self.ballPos == self.keeperPos:
            return True
        return False
