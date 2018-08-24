"""
@author  Mateus Paiva Matiazzi
"""

import time

class PID:

    def __init__(self, kp=1.0, ki=0.0, kd=0.0, maxIntegral=1000.0, maxDerivative=1000.0, target=0.0):
        # Constants 
        self.kp = kp
        self.ki = ki
        self.kd = kd

        # Max integral and derivative value
        self.maxIntegral = maxIntegral 
        self.maxDerivative = maxDerivative

        # Derivative e integral value
        self.derivative = 0.0
        self.integral = 0.0

        # SetPoint
        self.target = target
        self.error = 0.0

        # Initialize time sample 
        self.lastTime = time.time()

    def setKp(self, num):
        self.kp = num

    def setKi(self, num):
        self.ki = num

    def setKd(self, num):
        self.kd = num

    def setTarget(self, num):
        self.setTarget = setTarget

    def getConstants(self):
        return self.kp, self.ki, self.kd    	

    def update(self, value):
        """Update the error value and return as float"""
        error = self.target - value

        timerAux = time.time()
        deltaTime = timerAux - self.lastTime

        # Calculating pid values
        proportional = error
        integral = self.integral + (self.error*deltaTime)
        derivative = (error - self.error)/deltaTime

        # Verify if integral value is greater than maxIntegral value
        if integral > self.maxIntegral:
            integral = self.maxIntegral

        # Verify if derivative value is greater than maxDerivative value
        if derivative > self.maxDerivative:
            derivative = self.maxDerivative

        # Output value
        output = self.kp*proportional + self.ki*integral + self.kd*derivative

        # Update values
        self.integral = integral
        self.derivative = derivative
        self.error = error
        self.lastTime = timerAux

        return output

    def reset(self):
        """Reset pid values"""
        self.derivative = 0.0
        self.integral = 0.0
        self.error = 0.0
        self.lastTime = time.time()