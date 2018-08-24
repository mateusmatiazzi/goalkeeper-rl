"""
@author  Mateus Paiva Matiazzi
"""

import numpy as np
from PID import PID
from auxiliary import angleBetween, distancePoints

class Movement():
    """Movement class return leftWheelSpeed(int), rightWheelSpeed(int), done(boolean)"""

    def __init__(self, error):
        self.pid = PID(kp=40.0, ki=0.0, kd=0.0)
        self.lastPos = np.array([0, 0])
        self.errorMargin = error

    def inGoalPosition(self, robotPosition, goalPosition):
        """Verify if the robot is in goal position and return a boolean of the result"""
        if distancePoints(robotPosition, goalPosition) <= self.errorMargin:
            return True
        return False

    def inGoalVector(self, robotVector, goalVector):
        """Verify if the robot is in goal vector and return a boolean of the result"""
        if abs(angleBetween(robotVector, goalVector, ccw=False)) <= 0.0349066: #2 degrees error
            return True
        return False

    def moveToPoint(self, robotPosition, robotVector, goalPosition, speed):
        """Recives robot position, robot direction vector, goal position and a speed.
        Return the speed os the wheel to follow the vector (goal - robot)
        """
        if self.inGoalPosition(robotPosition, goalPosition):
            return 0, 0, True
        if any(self.lastPos != goalPosition):
            self.pid.reset()
        directionVector = goalPosition - robotPosition
        return self.followVector(robotVector, directionVector, speed) 

    def followVector(self, robotVector, goalVector, speed):
        """Recives the robot vector, goal vector and a speed and return the speed
        of the wheels to follow the goal vector"""
        diffAngle = angleBetween(robotVector, goalVector, ccw=False) 
        correction = self.pid.update(diffAngle)
        return self.returnSpeed(speed, correction)

    def spin(self, speed, ccw=True):
        """Recives a speed and a boolean counterclockwise and return the left wheel speed,
        right wheel speed and a boolean. Spin the robot"""
        if ccw:
            return int(-speed), int(speed), False
        return int(speed), int(-speed), False

    def headTo(self, robotVector, goalVector, speed):
        """Recives robot direction vector, goal vector and a speed. Return the left wheels speed,
        right wheel speed and done. Robot vector and goal vector will be parallels vectors."""
        diffAngle = angleBetween(robotVector, goalVector, ccw=False)
        if self.inGoalVector(robotVector, goalVector):
            return 0, 0, True
        correction = self.pid.update(diffAngle)
        if correction < 0:
            return int(speed+correction), 0, False
        return 0, int(speed-correction), False

    def returnSpeed(self, speed, correction):
        """Recives the robot speed and the PID correction, and return each wheel speed."""
        if speed < 0: #backwards
            if correction < 0:
                return int(speed + correction), int(speed), False
            return int(speed), int(speed - correction), False
        else: #forward
            if correction < 0:
                return int(speed), int(speed + correction), False
            return int(speed - correction), int(speed), False

    def forward(self, robotPosition, goalPosition ,speed): 
        """Recives a speed and make the robot go in forward direction""" 
        if self.inGoalPosition(robotPosition, goalPosition): 
            return 0, 0, True 
        return int(speed), int(speed), False