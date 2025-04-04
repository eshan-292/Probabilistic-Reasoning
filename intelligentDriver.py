# Prevent infinte recursion in the case of inifnte looping in motion of car


'''
Licensing Information: Please do not distribute or publish solutions to this
project. You are free to use and extend Driverless Car for educational
purposes. The Driverless Car project was developed at Stanford, primarily by
Chris Piech (piech@cs.stanford.edu). It was inspired by the Pacman projects.
'''
import util
import itertools
from turtle import Vec2D
from engine.const import Const
from engine.vector import Vec2d
from engine.model.car.car import Car
from engine.model.layout import Layout
from engine.model.car.junior import Junior
from configparser import InterpolationMissingOptionError

# Class: Graph
# -------------
# Utility class
class Graph(object):
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

# Class: IntelligentDriver
# ---------------------
# An intelligent driver that avoids collisions while visiting the given goal locations (or checkpoints) sequentially. 
class IntelligentDriver(Junior):

    # Funciton: Init
    def __init__(self, layout: Layout):
        self.burnInIterations = 30
        self.layout = layout 
        # self.worldGraph = None
        self.worldGraph = self.createWorldGraph()
        self.checkPoints = self.layout.getCheckPoints() # a list of single tile locations corresponding to each checkpoint
        self.transProb = util.loadTransProb()
        self.iter = 1

        
    # ONE POSSIBLE WAY OF REPRESENTING THE GRID WORLD. FEEL FREE TO CREATE YOUR OWN REPRESENTATION.
    # Function: Create World Graph
    # ---------------------
    # Using self.layout of IntelligentDriver, create a graph representing the given layout.
    def createWorldGraph(self):
        nodes = []
        edges = []
        # create self.worldGraph using self.layout
        numRows, numCols = self.layout.getBeliefRows(), self.layout.getBeliefCols()

        # NODES #
        ## each tile represents a node
        nodes = [(x, y) for x, y in itertools.product(range(numRows), range(numCols))]
        
        # EDGES #
        ## We create an edge between adjacent nodes (nodes at a distance of 1 tile)
        ## avoid the tiles representing walls or blocks#
        ## YOU MAY WANT DIFFERENT NODE CONNECTIONS FOR YOUR OWN IMPLEMENTATION,
        ## FEEL FREE TO MODIFY THE EDGES ACCORDINGLY.

        ## Get the tiles corresponding to the blocks (or obstacles):
        blocks = self.layout.getBlockData()
        blockTiles = []
        for block in blocks:
            row1, col1, row2, col2 = block[1], block[0], block[3], block[2] 
            # some padding to ensure the AutoCar doesn't crash into the blocks due to its size. (optional)
            row1, col1, row2, col2 = row1-1, col1-1, row2+1, col2+1
            blockWidth = col2-col1 
            blockHeight = row2-row1 

            for i in range(blockHeight):
                for j in range(blockWidth):
                    blockTile = (row1+i, col1+j)
                    blockTiles.append(blockTile)

        ## Remove blockTiles from 'nodes'
        nodes = [x for x in nodes if x not in blockTiles]

        for node in nodes:
            x, y = node[0], node[1]
            adjNodes = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
            
            # only keep allowed (within boundary) adjacent nodes
            adjacentNodes = []
            for tile in adjNodes:
                if tile[0]>=0 and tile[1]>=0 and tile[0]<numRows and tile[1]<numCols:
                    if tile not in blockTiles:
                        adjacentNodes.append(tile)

            for tile in adjacentNodes:
                edges.append((node, tile))
                edges.append((tile, node))
        return Graph(nodes, edges)

    #######################################################################################
    # Function: Get Next Goal Position
    # ---------------------
    # Given the current belief about where other cars are and a graph of how
    # one can driver around the world, chose the next position.
    #######################################################################################
    
    def getNextGoalPos(self, beliefOfOtherCars: list, parkedCars:list , chkPtsSoFar: int):
        '''
        Input:
        - beliefOfOtherCars: list of beliefs corresponding to all cars
        - parkedCars: list of booleans representing which cars are parked
        - chkPtsSoFar: the number of checkpoints that have been visited so far 
                       Note that chkPtsSoFar will only be updated when the checkpoints are updated in sequential order!
        
        Output:
        - goalPos: The position of the next tile on the path to the next goal location.
        - moveForward: Unset this to make the AutoCar stop and wait.

        Notes:
        - You can explore some files "layout.py", "model.py", "controller.py", etc.
         to find some methods that might help in your implementation. 
        '''
        goalPos = (0, 0) # next tile 
        moveForward = True

        currPos = self.getPos() # the current 2D location of the AutoCar (refer util.py to convert it to tile (or grid cell) coordinate)
        
        # BEGIN_YOUR_CODE 


        #self.iter +=1

    

        if True:
            col = util.xToCol(currPos[0])
            row = util.yToRow(currPos[1])

            G = self.worldGraph
            nodes = G.nodes
            
            currNode = (0,0)

            for node in nodes:
                if node[0] == row and node[1] == col:
                    currNode = node
                    break
            
            print("currNode: ", currNode)

            # get the next checkpoint
            nextChkPt = self.checkPoints[chkPtsSoFar]
            nextChkPtNode = (0,0)
            for node in nodes:
                #node.getPos()
                # if node[0] == nextChkPt[1] and node[1] == nextChkPt[0]:
                #     nextChkPtNode = node
                #     break                
                if node[0] == nextChkPt[0] and node[1] == nextChkPt[1]:
                    nextChkPtNode = node
                    break

            print("nextChkPtNode: ", nextChkPtNode)

            def getProbOfNode(row, col):
                prob = 0
                for b in beliefOfOtherCars:
                    prob += b.grid[row][col]
                return prob

            def getThreat(row, col):
                threat = 0
                count = 0
                for i in range(-1,2):
                    for j in range(-1,2):
                        if row+i >= 0 and row+i < self.layout.getBeliefRows() and col+j >= 0 and col+j < self.layout.getBeliefCols():
                            if(isobstacle(row+i, col+j)):
                                threat += 0.3
                            else:
                                threat += getProbOfNode(row+i, col+j)
                            count += 1
                threat += 3 * getProbOfNode(row, col)
                return threat/count
                
            parent_dict = {}

            def isobstacle(row,col):
                if (row,col) in G.nodes:
                    return True
                return False
                    

            # BFS on the graph
            
            def bfs(currNode, nextChkPtNode):
                visited = []
                queue = []
                queue.append(currNode)

                parent_dict[currNode] = None 

                #visited.append(currNode)
                s = currNode

                while queue:
                    s = queue.pop(0)
                    visited.append(currNode)
                    if s == nextChkPtNode:
                        # Goal Found Exit from BFS
                        break 
                    
                    possible_neighbors = []
                    for edge in G.edges:
                        if edge[0] == s and edge[1] not in visited:
                            possible_neighbors.append(edge[1])
                            # queue.append(edge[1])
                            # visited.append(edge[1])
                            # parent_dict[edge[1]] = s
                    
                    node_dict = {}       # Dictionary mapping nodes to the probability of any car being in that node
                    for n in possible_neighbors:
                        prob = 0
                        for b in beliefOfOtherCars:
                            row = node[0]
                            col = node[1]
                            prob += b.grid[row][col]
                        node_dict[n] = prob
                    
                    l = sorted(node_dict.items(), key = lambda x : x[1])

                    for (a,b) in l:
                        queue.append(a)
                        visited.append(a)
                        parent_dict[a] = s


                # Backtrack to get the path
                path = []
                path.append(s)
                
                while parent_dict[s] != None:
                    path.append(parent_dict[s])
                    s = parent_dict[s]
                    
                return path

            path = bfs(currNode, nextChkPtNode)
            try:
                goalnode = path[-2]
                p = getProbOfNode(goalnode[0], goalnode[1])
                if p > 0.1:
                    neighbors = []
                    for edge in G.edges:
                        if edge[0] == currNode:
                            neighbors.append(edge[1])

                    min_prob = 10
                    min_neighbor = None
                    for n in neighbors:
                        p = getThreat(n[0], n[1])
                        if p < min_prob:
                            min_prob = p
                            min_neighbor = n

                    goalnode = min_neighbor
                goalPos = (util.colToX(goalnode[1]), util.rowToY(goalnode[0]))

                print("GOAL STATE -> ", "(",goalnode[0] ,",",goalnode[1], ")") 
                
                # if getProbOfNode(goalnode[0], goalnode[1])>0.1:
                #     self.iter+=1
                #     if self.iter%2!=0:
                #         moveForward = False
                #         print("Move Forward -> ", moveForward )                
                    

            except:
                moveForward = False
                print("Move Forward -> ", moveForward )                

        else:
            moveForward = False

        # END_YOUR_CODE
        return goalPos, moveForward

    # def getProbOfNode(row, col, beliefOfOtherCars):
    #     prob = 0
    #     for b in beliefOfOtherCars:
    #         prob += b.grid[row][col]

    #     return prob

    # DO NOT MODIFY THIS METHOD !
    # Function: Get Autonomous Actions
    # --------------------------------
    def getAutonomousActions(self, beliefOfOtherCars: list, parkedCars: list, chkPtsSoFar: int):
        # Don't start until after your burn in iterations have expired
        if self.burnInIterations > 0:
            self.burnInIterations -= 1
            return[]
       
        goalPos, df = self.getNextGoalPos(beliefOfOtherCars, parkedCars, chkPtsSoFar)
        vectorToGoal = goalPos - self.pos
        wheelAngle = -vectorToGoal.get_angle_between(self.dir)
        driveForward = df
        actions = {
            Car.TURN_WHEEL: wheelAngle
        }
        if driveForward:
            actions[Car.DRIVE_FORWARD] = 1.0
        return actions
    
    