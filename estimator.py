# Vary the total number of particles 
# Find a way to emulate the transitions of the car
# Use adaptive particle filtering
# handle parked cars
# x, y -> pixel values
# set variance value to something nice
# 


import util 
import numpy as np
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
                        
        # Initialisation based on previous belief values
        numParticles = 1000
        numRows = self.belief.numRows
        numCols = self.belief.numCols
        width = numCols * Const.BELIEF_TILE_SIZE
        height = numRows * Const.BELIEF_TILE_SIZE
        # prob = np.array(self.belief.grid).flatten(order = 'C') 

        # Sampling x and y coordinates of particles based on the probablity distribution calculated until now
        # coords = [(i, j) for i in range(numRows) for j in range(numCols)]
        # particles = np.random.choices(coords, weights = prob, k = numParticles)

        # coords = np.random.choice(numRows * numCols, numParticles, p=prob)
        # coords = random.choices(range(numRows * numCols), k = numParticles, weights = prob)
        # particles = [[util.colToX(coords[i]%numCols), util.rowToY(coords[i]//numCols), prob[coords[i]]] for i in range(numParticles)]      # List of particles represented as (x, y, w), where x and y are the columns and row numbers and w is the corresponding weight of the particle (in range of 0 to 1)

        particles = []
        for row in range(numRows):
            for col in range(numCols):
                w = self.belief.grid[row][col]
                n = int(w * numParticles)
                for i in range(n):
                    particles.append([util.colToX(col), util.rowToY(row), w])
        # Moving the particles probablistically based on the transition probabilities
        numParticles = len(particles)
        # Estimating the position of car based on probability distribution calculated till now
        
        if not isParked:
            for i in range(numParticles):
                x, y, w = particles[i]
                col = util.xToCol(x)
                row = util.yToRow(y)
                try: 
                    pl = self.transProb[((row,col),(row-1, col))]
                except:
                    pl = 0
                try: 
                    pr = self.transProb[((row,col),(row+1, col))]
                except:
                    pr = 0
                try:
                    pu = self.transProb[((row,col),(row, col-1))]
                except:
                    pu = 0
                try:
                    pd = self.transProb[((row,col),(row, col+1))]
                except:
                    pd = 0

                try:
                    ps = self.transProb[((row,col),(row, col))]
                except:
                    ps = 0


                if pl == 0 and pr == 0 and pu == 0 and pd == 0 and ps==0 :
                    pl = 0.2
                    pu = 0.2
                    pr = 0.2
                    pd = 0.2
                    ps = 0.2

                # try:
                #     plu = self.transProb[((row,col),(row-1, col+1))]
                # except:
                #     plu = 0
                # try:
                #     pur = self.transProb[((row,col),(row+1, col+1))]
                # except:
                #     pur = 0
                # try:
                #     prd = self.transProb[((row,col),(row+1, col-1))]
                # except:
                #     prd = 0
                # try:
                #     pdl = self.transProb[((row,col),(row-1, col-1))]
                # except:
                #     pdl = 0
                
                # pdl = 1 - pl - pu - pr - pd - plu - pur - prd 
                    
                #pd = 1 - pl - pr - pu
                # except:
                #     pl = 0.25
                #     pr = 0.25
                #     pu = 0.25
                #     pd = 0.25
                    # plu = 0.125
                    # pur = 0.125
                    # prd = 0.125
                    # pdl = 0.125

                # print(row, col)
                # print(pl, pr, pu, pd, ps)
                
                
                move = random.choices(range(5), weights=[pl, pu, pr, pd, ps], k = 1)
                
                if move == 0:
                    if particles[i][0]-(1* Const.BELIEF_TILE_SIZE) >= 0:
                        particles[i][0] -= 1 * Const.BELIEF_TILE_SIZE
                elif move == 1:
                    if particles[i][1]+(1* Const.BELIEF_TILE_SIZE) <= height-1:
                        particles[i][1] += 1* Const.BELIEF_TILE_SIZE
                elif move == 2:
                    if particles[i][0]+(1* Const.BELIEF_TILE_SIZE) <= width-1:
                        particles[i][0] += 1* Const.BELIEF_TILE_SIZE
                elif move == 3:
                    if particles[i][1]-(1* Const.BELIEF_TILE_SIZE) >= 0:
                        particles[i][1] -= 1* Const.BELIEF_TILE_SIZE
                    
                    
                # elif move == 4:
                #     if particles[i][0]-(1* Const.BELIEF_TILE_SIZE) >= 0 and particles[i][1]+(1* Const.BELIEF_TILE_SIZE) <= height-1:
                #         particles[i][0] -= 1* Const.BELIEF_TILE_SIZE
                #         particles[i][1] += 1* Const.BELIEF_TILE_SIZE

                # elif move == 5:
                #     if particles[i][1]+(1* Const.BELIEF_TILE_SIZE) <= height-1 and particles[i][0]+(1* Const.BELIEF_TILE_SIZE) <= width-1:
                #         particles[i][1] += 1* Const.BELIEF_TILE_SIZE
                #         particles[i][0] += 1* Const.BELIEF_TILE_SIZE

                # elif move == 6:
                #     if particles[i][0]+(1* Const.BELIEF_TILE_SIZE) <= width-1 and particles[i][1]-(1* Const.BELIEF_TILE_SIZE) >= 0:
                #         particles[i][0] += 1* Const.BELIEF_TILE_SIZE
                #         particles[i][1] -= 1* Const.BELIEF_TILE_SIZE
                # else:
                #     if particles[i][0]-(1* Const.BELIEF_TILE_SIZE) >= 0 and particles[i][1]-(1* Const.BELIEF_TILE_SIZE) >= 0:
                #         particles[i][1] -= 1* Const.BELIEF_TILE_SIZE
                #         particles[i][0] -= 1* Const.BELIEF_TILE_SIZE
                

        # Recalculating weights based on the observed distance
        for i in range(len(particles)):
            x, y, w  =  particles[i]
            d = math.sqrt((x-posX)*(x-posX) + (y-posY)*(y-posY))
            particles[i][2] = util.pdf(mean = d, std = Const.SONAR_STD, value = observedDist)
            
        # Normalising the probability distribution
        grid  = [[0 for _ in range(numCols)] for _ in range(numRows)]

        for (x, y, w) in particles:
            # print(x, y, w)
            row = util.yToRow(y)
            col = util.xToCol(x)
            grid[row][col] += w
        
        self.belief.grid = grid
        self.belief.normalize()

        print("GRID: ", self.belief.grid)
        # END_YOUR_CODE
        return
        
        
        
        
        
        t = util.loadTransProb()
        # print("FULL DICT: ", t)
        print("START")
        i = 0
        for k in t:
            i = i+1
            a,b = k
            for (x,y) in t.keys():
                if x==a and y!=b and  t[(x, y)] !=0 :
                    print(x, ", ", y, " -> ", t[(x, y)] )
            if i==5:
                break

        print("END")
        #print("Trans Prob Dict: ", t[((0,0), (0,1))])
  
    def getBelief(self) -> Belief:
        return self.belief
        
class Particle:
    def __init__(self, row, col, weight) -> None:
        self.row = row
        self.col = col
        self.weight = weight

    def __repr__(self) -> str:
        return f"Particle(row={self.row}, col={self.col}, weight={self.weight})"

    def transition(self, move, numRows, numCols) -> None:
        """Update the particle's position based on the given action and the grid."""
        
        row = self.row
        col = self.col
        
        try: 
                pl = self.transProb[((row,col),(row-1, col))]
                pr = self.transProb[((row,col),(row+1, col))]
                pu = self.transProb[((row,col),(row, col-1))]
                #pd = self.transProb[((row,col),(row, col+1))]
                pd = 1 - pl - pr - pu
        except:
                pl = 0.25
                pr = 0.25
                pu = 0.25
                pd = 0.25

        move = np.random.choice(4, p=[pl, pu, pr, pd])


        if move == 0:
            if row-1 >= 0:
                    self.row -= 1
                    
            elif move == 1:
                if col+1 <= numRows-1:
                    self.col += 1
            elif move == 2:
                if row+1 <= numCols-1:
                    self.row += 1
            else:
                if col-1 >= 0:
                    self.col -= 1


        raise Exception("Not implemented yet")
        # END_YOUR_CODE