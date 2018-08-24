"""
@author  Mateus Paiva Matiazzi
"""

import numpy as np
import csv

def returnState(pos):
    """Return ball and robot states"""
    if pos[1] < 200:
        return 0
    elif pos[1] > 390:
        return 11
    else:
        return int((pos[1] - 200)/16)

def initializeTable(filePath):
    """Initialize q Table in filePath and return it"""
    aux = []
    with open(filePath) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            aux.append(map(float, row))
    return aux

def qState(table, robotState, ballState):
    """Return the state to search in table"""
    return table[12 * ballState + robotState]

def getAction(row):
    """Return the best action in row"""
    return np.argmax(row) - 2

def returnNewRobotPos(robotPos, action):
    """Return the new pos"""
    return np.array([robotPos[0], robotPos[1] + action * 16])