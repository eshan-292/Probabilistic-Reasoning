# Vary the total number of particles 
# Use a better Inverse Function
# FInd a way to emulate the transitions of the car
# Use adaptive particle filtering


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
        # X = np.random.randint(0, numCols, (numParticles, 1))
        # Y = np.random.randint(0, self.belief.numRows, (numParticles, 1))

        # particles = [(X[i], Y[i], 1/numParticles) for i in range(numParticles)]      # List of particles represented as (x, y, w), where x and y are the columns and row numbers and w is the corresponding weight of the particle (in range of 0 to 1)

        
        # Initialisation based on previous belief values
        numParticles = 100
        numRows = self.belief.numRows
        numCols = self.belief.numCols
        prob = np.array(self.belief.grid).flatten() 

        # Sampling x and y coordinates of particles based on the probablity distribution calculated until now
        # coords = [(i, j) for i in range(numRows) for j in range(numCols)]
        # particles = np.random.choices(coords, weights = prob, k = numParticles)

        coords = np.random.choice(numRows * numCols, numParticles, p=prob)
        particles = [[coords[i]%numCols, coords[i]//numCols, prob[coords[i]]] for i in range(numParticles)]      # List of particles represented as (x, y, w), where x and y are the columns and row numbers and w is the corresponding weight of the particle (in range of 0 to 1)
        # print(particles)
        # X = coords//numCols
        # Y = coords%numCols


        # Moving the particles probabblistically based on the transition probabilities

        # Estimating the position of car based on probability distribution calculated till now
        
        # estimated_pos = coords[np.argmax(prob)]
        # row = estimated_pos//numCols
        # col = estimated_pos%numCols

        # print(self.transProb)
        # # pl = self.transProb[((row,col),(row-1, col))] if row-1>=0 else 0
        # try: 
        #     pl = self.transProb[((row,col),(row-1, col))]
        # except:
        #     pl = 0
        # # pr = self.transProb[((row,col),(row+1, col))] if row+1<numRows else 0
        # try:
        #     pr = self.transProb[((row,col),(row+1, col))]
        # except:
        #     pr = 0
        # # pu = self.transProb[((row,col),(row, col-1))] if col-1>=0 else 0
        # try:
        #     pu = self.transProb[((row,col),(row, col-1))]
        # except:
        #     pu = 0
        # # pd = self.transProb[((row,col),(row, col+1))] if y+1<numCols else 0
        # try:
        #     # pd = self.transProb[((row,col),(row, col+1))]
        #     pd = 1 - pl - pr - pu
        # except:
        #     pd = 0

        # # if math.isnan(pl):
        # #     pl = 1 - pr - pu - pd
        # # if math.isnan(pr):
        # #     pr = 1 - pl - pu - pd
        # # if math.isnan(pu):
        # #     pu = 1 - pl - pr - pd
        # # if math.isnan(pd):
        # #     pd = 1 - pl - pr - pu

        # moves = np.random.choice(4, numParticles, p=[pl, pu, pr, pd])
        # for i in range(numParticles):
        #     if moves[i] == 0:
        #         particles[i][0] -= 1
        #     elif moves[i] == 1:
        #         particles[i][1] += 1
        #     elif moves[i] == 2:
        #         particles[i][0] += 1
        #     else:
        #         particles[i][1] -= 1
                
        # Recalculating weights based on the observed distance
        sum = 0
        for i in range(len(particles)):
            x, y, w  =  particles[i]
            d = math.sqrt((x-autocar_x)*(x-autocar_x) + (y-autocar_y)*(y-autocar_y))
            particles[i][2] = abs(d-observedDist)
            sum += abs(d-observedDist)
            
        # W = np.abs(np.sqrt((X-autocar_x)*(X-autocar_x) + (Y-autocar_y)*(Y-autocar_y)) - observedDist)
        # sum = np.sum(W)

        # Calculating the probability distribution by inverting the weights for each particle 
        new_sum = 0
        for i in range(len(particles)):
            particles[i][2] = sum - particles[i][2] 
            new_sum += particles[i][2]

        # Normalising the probability distribution
        
        grid  = [[0 for _ in range(numCols)] for _ in range(numRows)]
        
        for (x, y, w) in particles:
        # for i in range(numParticles):
            # self.belief.setProb(X[i], Y[i], (sum - W[i]))
            grid[y][x] += (w)/(new_sum)
        
        # self.belief.normalize()
        self.belief.grid = grid

        print("GRID: ", self.belief.grid)
        

        # END_YOUR_CODE
        return
  
    def getBelief(self) -> Belief:
        return self.belief
