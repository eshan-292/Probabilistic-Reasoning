# Use adaptive particle filtering
# handle parked cars
# x, y -> pixel values - randomly generate particles
# optimize table computation

import util 
from util import Belief, pdf 
from engine.const import Const
import math
import random

# Class: Estimator
#----------------------
# Maintain and update a belief distribution over the probability of a car being in a tile.
class Estimator(object):
    def __init__(self, numRows: int, numCols: int):
        self.belief = util.Belief(numRows, numCols) 
        self.transProb = util.loadTransProb() 
        # self.particles = []
        self.table = self.computeTransTable()
        self.numIterations = 0
        
        
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
        numRows = self.belief.numRows
        numCols = self.belief.numCols

        numParticles = numCols * numRows * 10
        # numParticles = numCols * numRows * 20 - numCols * self.numIterations

        # if(numParticles < numCols * numRows):
        #     numParticles = numCols * numRows

        
        # Sampling x and y coordinates of particles based on the probablity distribution calculated until now
        prob = [self.belief.getProb(i, j) for i in range(numRows) for j in range(numCols)]
        coords = random.choices(range(numRows * numCols), k = numParticles, weights = prob)
        particles = [[util.colToX(coords[i]%numCols), util.rowToY(coords[i]//numCols)] for i in range(numParticles)]      # List of particles represented as (x, y, w), where x and y are the columns and row numbers and w is the corresponding weight of the particle (in range of 0 to 1)

        # coords = [(i, j) for i in range(numRows) for j in range(numCols)]
        # particles = random.choices(coords, weights = prob, k = numParticles)

        # Estimating the position of car based on probability distribution calculated till now
        if not isParked:
            for i in range(numParticles):
                x, y = particles[i]
                col = util.xToCol(x)
                row = util.yToRow(y)      

                try:
                    neighbors_prob = self.table[(row,col)]
                    dest = random.choices(list(neighbors_prob.keys()), weights = list(neighbors_prob.values()), k = 1)[0]
                    particles[i][0] = util.colToX(dest[1])
                    particles[i][1] = util.rowToY(dest[0])
                except:
                    pass

        # Recalculating weights based on the observed distance
        grid  = [[0 for _ in range(numCols)] for _ in range(numRows)]

        for i in range(len(particles)):
            x, y  =  particles[i]
            col = util.xToCol(x)
            row = util.yToRow(y)
            d = math.sqrt((x-posX)*(x-posX) + (y-posY)*(y-posY))
            grid[row][col] += util.pdf(mean = d, std = Const.SONAR_STD, value = observedDist)
            
        self.belief.grid = grid
        # Normalising the probability distribution
        self.belief.normalize()

        # incrementing the number of iterations for adaptive particle filtering
        self.numIterations += 1                
        # END_YOUR_CODE
        return
  
    def getBelief(self) -> Belief:
        return self.belief

    def computeTransTable(self):    
        t = self.transProb
        table = {}

        for (a,b) in t.keys():
            neighbors_prob = {}
            for (x,y) in t.keys():
                if x==a  and  t[(x, y)] !=0 :
                    neighbors_prob[y] = t[(x, y)]
                    # print(x, ", ", y, " -> ", t[(x, y)] )
            table[a] = neighbors_prob

        return table

    # def trans(self, grid_pos):    
    #     neighbors_prob = {}
    #     t = self.transProb
    #     # print("FULL DICT: ", t)
    #     # print("START")
    #     i = 0
    #     for k in t:
    #         i = i+1
    #         a,b = k
    #         if a==grid_pos:
    #             for (x,y) in t.keys():
    #                 if x==a  and  t[(x, y)] !=0 :
    #                     neighbors_prob[y] = t[(x, y)]
    #                     print(x, ", ", y, " -> ", t[(x, y)] )
            
    #     return neighbors_prob

    # def ispossible(self, grid_pos):
    #     if grid_pos[0]>=0 and grid_pos[0]<self.belief.numRows and grid_pos[1]>=0 and grid_pos[1]<self.belief.numCols:
    #         return True
    #     return False        
class Particle:
    def __init__(self, row, col, weight) -> None:
        self.row = row
        self.col = col
        self.weight = weight

    def __repr__(self) -> str:
        return f"Particle(row={self.row}, col={self.col}, weight={self.weight})"

    # def transition(self, move, numRows, numCols) -> None:
    #     """Update the particle's position based on the given action and the grid."""
        
    #     row = self.row
    #     col = self.col
        
    #     try: 
    #             pl = self.transProb[((row,col),(row-1, col))]
    #             pr = self.transProb[((row,col),(row+1, col))]
    #             pu = self.transProb[((row,col),(row, col-1))]
    #             #pd = self.transProb[((row,col),(row, col+1))]
    #             pd = 1 - pl - pr - pu
    #     except:
    #             pl = 0.25
    #             pr = 0.25
    #             pu = 0.25
    #             pd = 0.25

    #     move = np.random.choice(4, p=[pl, pu, pr, pd])


    #     if move == 0:
    #         if row-1 >= 0:
    #                 self.row -= 1
                    
    #         elif move == 1:
    #             if col+1 <= numRows-1:
    #                 self.col += 1
    #         elif move == 2:
    #             if row+1 <= numCols-1:
    #                 self.row += 1
    #         else:
    #             if col-1 >= 0:
    #                 self.col -= 1


    #     raise Exception("Not implemented yet")
    #     # END_YOUR_CODE