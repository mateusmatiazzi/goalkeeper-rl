"""
@author  Mateus Paiva Matiazzi
"""

from src.simulator.simulator import Simulator
from src.simulator.movement import Movement
from src.rl.environment import Environment
from src.rl.rlSimulator import *
from src.simulator.auxiliary import throwInGoal
import cv2
import random

robotInitPosition = (120,200)
ballInitPosition = (680, random.randint(80, 530))
# Rl delay
FRAME = 5

def printInformation():
    print "**********************************************"
    print "Initializing reinforcement learning simulation"
    print "                  Goalkeeper                  "
    print "**********************************************"
    print "Press any key to start:"
    print "To execute random actions press: r"
    print "To exit the simulation press: q"

if __name__ == "__main__":
    printInformation()

    env = Environment(12)
    randomMode = False

    goalShoot = 0
    defense = 0

    # window size
    img = np.zeros((600,800,3), np.uint8)
    # creating simulator
    sim = Simulator(img)
    # initialize arena
    sim.initArena()
    # initialize robot in goal
    sim.drawRobot(robotInitPosition, [0,1])
    # initialize ball
    sim.drawBall(ballInitPosition)

    # throwVector
    throwVector = throwInGoal(530, 60, sim.ball)

    # initialize movement class
    movement = Movement(10)

    # initialize qTable
    qTable = initializeTable('./results/Qtable.csv')

    # show img
    cv2.imshow('Goalkeeper Simulation',img)
    cv2.moveWindow('Goalkeeper Simulation', 400,0)

    key = cv2.waitKey(0)
    actionFrame = 0
    while 1:
        cv2.imshow('Goalkeeper Simulation',img)
        cv2.moveWindow('Goalkeeper Simulation', 400,0)

        # End simulation
        if key == ord('q'):
            cv2.destroyAllWindows()
            break

        # Rl delay
        if actionFrame % FRAME == 0:
            # get robotState
            robotState = returnState(sim.robot)
            env.setKeeperPos(robotState)
            # get ballState
            ballState = returnState(sim.ball)
            # get row in table
            stateRow = qState(qTable, robotState, ballState)
            # get Action
            action = getAction(stateRow)
            # random action
            if randomMode:
                action = random.choice(env.listOfActions())
            # recive new robotPos
            newPos = returnNewRobotPos(sim.robot, action)
            actionFrame = 0

        if key == ord('r'):
            randomMode = not randomMode

        # movement
        if sim.robot[1] > newPos[1]:
            leftSpeed, rightSpeed, done = movement.forward(np.array(sim.robot), np.array(newPos), -130)
        else:
            leftSpeed, rightSpeed, done = movement.forward(np.array(sim.robot), np.array(newPos), 130)

        # ball movment
        sim.throwBall(throwVector, 150)

        if not done:
            # move function
            sim.move(leftSpeed,rightSpeed)

        if sim.ball[0] <= 165:
            if sim.ball[1] >= 220 and sim.ball[1] <= 380:
                goalShoot += 1
                if abs(sim.robot[1]-sim.ball[1]) < 16:
                    defense += 1
            sim.drawBall((680, random.randint(80, 530)))
            throwVector = throwInGoal(400, 200, sim.ball)

        # 60fps
        key = cv2.waitKey(16)
        actionFrame += 1

    print "Goal Shoots", goalShoot
    print "Defense Percentage", defense*100/goalShoot,"%"