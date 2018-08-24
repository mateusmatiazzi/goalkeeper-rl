"""
@author  Mateus Paiva Matiazzi
"""

class Q(object):
    
    def __init__(self, alpha=0.1, gamma=0.9):
        self.alpha = alpha
        self.gamma = gamma

    def setGamma(self, newGamma):
        self.gamma = newGamma

    def setAlpha(self, newAlpha):
        self.alpha = newAlpha

    def learn(self, s, r, s_):
        return (1-self.alpha)*s + self.alpha*(r + self.gamma*s_)