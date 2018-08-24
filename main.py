"""
@author  Mateus Paiva Matiazzi
"""

from src.rl.environment import Environment
from src.rl.qLearning import Q
from src.rl.valueTable import ValueTable
from src.rl.greedyExplorer import GreedyExplorer
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import csv

# initialize environment and the learner
env = Environment(arenaStates=12, numberActions=5)
learner = Q(alpha=0.1, gamma=0.9)
table = ValueTable(env._numberStates(), env._numberActions())

#initialize table with 0
table.initializeTable(initValue=0.0)
explorer = GreedyExplorer(goalEnvironment=env, valueTable=table, epsilon=0.30, decay=1)

print "**********************************************"
print "Initializing reinforcement learning training"
print "                  Goalkeeper                  "
print "**********************************************"
print "\n1 - Simulate all states"
print "2 - Plot one ball state"
print "3 - Plot accumulated reward\n"

option = int(raw_input("Option: "))

if option == 1 or option == 3:
    ballInPosNumber = 12
elif option ==2:
    ballInPosNumber = 1
    explorer.updateDecay(0.8)

episodesNumber = int(raw_input("Enter the number of episodes:"))

#initizlize defense positions
for i in range(12):
    table.updateTable(12*i+i, 2, 100)

stepsList = []
mseList = []
accumulatedReward = []
stepmax = -1

# Qlearning
for ballInPos in range(ballInPosNumber):
    env.setBallPos(ballInPos)
    explorer.updateEpsilon(0.3)
    for i in range(episodesNumber):
        if option == 1 or option == 3:
            env.randomKeeper()
        else:
            env.keeperPos = 11
        steps = 0
        oldTable = table.returnTable().copy()
        while 1:
            state = env.returnState()
            action = explorer.chooseAction()
            env.performAction(action)
            reward = env.getReward()
            newState = env.returnState()
            table.updateTable(state, action+2, learner.learn(table.stateValue(state, action+2), reward, table.maxState(newState)))
            steps += 1
            if env.isGoal():
                break
        explorer.useDecay()
        newTable = table.returnTable().copy()
        accumulatedReward.append(table.returnTable().sum())  
        # print "Episode :", i+1, ", number of steps:", steps
        mseList.append(mean_squared_error(oldTable, newTable))
        
        # Number max of steps
        if steps > stepmax:
            stepmax = steps

        stepsList.append(steps)

# Plot Q table in csv file
if option == 1:
    csvFile = open('Qtable.csv', 'w')
    with csvFile:
        writer = csv.writer(csvFile)
        for row in table.returnTable():
            aux = map(np.float16, row)
            writer.writerow(aux)
    print "Training Done"
    print "Qtable.csv generated"
# Plot MSE error
elif option==2:
    x = np.arange(1, episodesNumber+1, 1)
    blue_patch = mpatches.Patch(color='blue', label='Steps')
    green_patch = mpatches.Patch(color='green', label='MSE')
    plt.plot(x, stepsList)
    plt.plot(x, [i*stepmax for i in mseList])
    plt.autoscale(tight=True)
    plt.legend(handles=[blue_patch, green_patch])
    plt.grid(True)
    plt.xlabel('Episodes')
    plt.savefig("steps_error.png")
    plt.show()
    print "Plot Done"
    print "steps_error.png generated"
# Plot accumulated reward
else:
    x = np.arange(1, 12*episodesNumber+1, 1)
    blue_patch = mpatches.Patch(color='blue', label='reward')
    plt.plot(x, accumulatedReward)
    plt.legend(handles=[blue_patch])
    plt.grid(True)
    plt.xlabel('Episodes')
    plt.savefig("accumulatedReward.png")
    plt.show()
    print "Plot Done"
    print "accumulatedReward.png generated"
