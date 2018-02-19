from random import randint
from BaseAI import BaseAI
import time
import sys

# Time Limit Before Losing
timeLimit = 0.2
allowance = 0.15

class PlayerAI(BaseAI):
    
    def getMove(self, grid):
        print "getMoveStart"
        sys.setrecursionlimit(2000)
        self.prevTime = time.clock()
        cells = grid.getAvailableCells()
        #Impliment Minimax algorithm
        (_, _, maxMove) = self.Maximize(grid.clone())
        print "getMoveStop: maxMove :" + str(maxMove)
        return maxMove

    def Maximize(self, grid):
        #If grid state is terminal, return the evaluated grid value
        timeAlmostUp = time.clock() - self.prevTime > timeLimit - allowance
        if (not grid.canMove()) or timeAlmostUp:
            return (None, self.Eval(grid), 0)
        
        #initialize max child and max Value
        (maxChild, maxValue, maxMove) = (None, float('-inf'), 0)
        
        #For each child (one for each possible move), Minimize and save child w/ Max value
        moveOrder = [0, 1, 2, 3]
        for move in moveOrder:
            child = grid.clone()
            isLegalMove = child.move(move)
            if isLegalMove:
                (_, childValue, _) = self.Minimize(child.clone())
                if childValue > maxValue:
                    (maxChild, maxValue, maxMove) = (child, childValue, move)
        
        #print "returning maxValue of: " + str(maxValue)
        return (maxChild, maxValue, maxMove)

    def Minimize(self, grid):
        #If grid state is terminal, return the evaluated grid value
        timeAlmostUp = time.clock() - self.prevTime > timeLimit - allowance
        if (not grid.canMove()) or timeAlmostUp:
            return (None, self.Eval(grid), 0)
        
        #initialize min child and min Value
        (minChild, minValue, minMove) = (None, float('inf'), 0)
        
        #For each child (one for each possible computer move), Maximize and save child w/ Min value
        i = 0
        cells = grid.getAvailableCells()
        if cells:
            while i < len(cells):
                move = cells[i]
                # Validate Move
                if move and grid.canInsert(move):
                    #try 2
                    twoChild = grid.clone()
                    twoChild.setCellValue(move, 2)
                    (_, twoChildValue, _) = self.Maximize(twoChild.clone())
                    if twoChildValue < minValue:
                            (minChild, minValue, minMove) = (twoChild, twoChildValue, 0)
                    #try 4
                    fourChild = grid.clone()
                    fourChild.setCellValue(move, 4)
                    (_, fourChildValue, _) = self.Maximize(fourChild.clone())
                    if fourChildValue < minValue:
                        (minChild, minValue, minMove) = (fourChild, fourChildValue, 0)
                i = i + 1
    
        #print "returning minValue of: " + str(minValue)
        return (minChild, minValue, minMove)

    def Eval(self, grid):
        return grid.getMaxTile()
