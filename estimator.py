import util 
import numpy as np
from util import Belief, pdf 
from engine.const import Const
import math

# Class: Estimator
#----------------------
# Maintain and update a belief distribution over the probability of a car being in a tile.
class Estimator(object):
    def __init__(self, numRows: int, numCols: int):
        self.belief = util.Belief(numRows, numCols) 
        self.transProb = util.loadTransProb() 
            
    ##################################################################################
    # [ Estimation Problem ]
    # Function: estimate (update the belief about a StdCar based on its observedDist)
    # ----------------------
    # Takes |self.belief| -- an object of class Belief, defined in util.py --
    # and updates it *inplace* based onthe distance observation and your current position.
    #
    # - posX: x location of AutoCar 
    # - posY: y location of AutoCar 
    # - observedDist: current observed distance of the StdCar 
    # - isParked: indicates whether the StdCar is parked or moving. 
    #             If True then the StdCar remains parked at its initial position forever.
    # 
    # Notes:
    # - Carefully understand and make use of the utilities provided in util.py !
    # - Remember that although we have a grid environment but \
    #   the given AutoCar position (posX, posY) is absolute (pixel location in simulator window).
    #   You might need to map these positions to the nearest grid cell. See util.py for relevant methods.
    # - Use util.pdf to get the probability density corresponding to the observedDist.
    # - Note that the probability density need not lie in [0, 1] but that's fine, 
    #   you can use it as probability for this part without harm :)
    # - Do normalize self.belief after updating !!

    ###################################################################################
    def estimate(self, posX: float, posY: float, observedDist: float, isParked: bool) -> None:
        # BEGIN_YOUR_CODE

        # Checking if car is stationary (parked)
        if isParked:
            return 
        
        autocar_x = util.xToCol(posX)
        autocar_y = util.yToRow(posY)
                
        # # Initialisation - Random uniform distribution 
        # numParticles = 100
        # X = np.random.randint(0, self.belief.numCols, (numParticles, 1))
        # Y = np.random.randint(0, self.belief.numRows, (numParticles, 1))

        # particles = [(X[i], Y[i], 1/numParticles) for i in range(numParticles)]      # List of particles represented as (x, y, w), where x and y are the columns and row numbers and w is the corresponding weight of the particle (in range of 0 to 1)

        
        # Initialisation based on previous belief values
        numParticles = 100
        prob = np.array(self.belief.grid).flatten() 

        # Sampling x and y coordinates of particles based on the probablity distribution calculated until now
        # coords = [(i, j) for i in range(self.belief.numRows) for j in range(self.belief.numCols)]
        # particles = np.random.choices(coords, weights = prob, k = numParticles)

        coords = np.random.choice(self.belief.numRows * self.belief.numCols, numParticles, p=prob)
        # particles = [[coords[i]//self.belief.numCols, coords[i]%self.belief.numCols, prob[coords[i]]] for i in range(numParticles)]      # List of particles represented as (x, y, w), where x and y are the columns and row numbers and w is the corresponding weight of the particle (in range of 0 to 1)
        # print(particles)
        X = coords//self.belief.numCols
        Y = coords%self.belief.numCols

        # Recalculating weights based on the observed distance
        # sum = 0
        # for i in range(len(particles)):
        #     x, y, w  =  particles[i]
        #     d = math.sqrt((x-autocar_x)*(x-autocar_x) + (y-autocar_y)*(y-autocar_y))
        #     particles[i][2] = abs(d-observedDist)
        #     sum += abs(d-observedDist)
            
        W = np.abs(np.sqrt((X-autocar_x)*(X-autocar_x) + (Y-autocar_y)*(Y-autocar_y)) - observedDist)
        sum = np.sum(W)

        # # Calculating the probability distribution by inverting the weights for each particle 
        # new_sum = 0
        # for i in range(len(particles)):
        #     particles[i][2] = sum - particles[i][2] 
        #     new_sum += particles[i][2]

        # Normalising the probability distribution
        
        # grid  = [[0 for i in range(self.belief.numCols)] for j in range(self.belief.numRows)]
        
        for i in range(numParticles):
            self.belief.setProb(X[i], Y[i], (sum - W[i]))
            # grid[x][y] += (sum - w)/((numParticles - 1)* sum)
        
        self.belief.normalize()
        # self.belief.grid = grid

        print("GRID: ", self.belief.grid)
        

        # END_YOUR_CODE
        return
  
    def getBelief(self) -> Belief:
        return self.belief

# Test case
# estimator = Estimator(3, 4)
# estimator.estimate(0, 0, 0, False)