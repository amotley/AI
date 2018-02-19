from random import randint
from BaseAI import BaseAI
import time
import sys

# Time Limit Before Losing
timeLimit = 0.2
buffer = 0.05

class PlayerAI(BaseAI):
    
    def getMove(self, grid):
        sys.setrecursionlimit(2000)
        self.prevTime = time.clock()
        cells = grid.getAvailableCells()
        #Impliment Minimax algorithm
        (_, _, maxMove) = self.Maximize(grid.clone(), float('-inf'), float('inf'), 0)
        return maxMove

    def Maximize(self, grid, alpha, beta, depth):
        #If grid state is terminal, return the evaluated grid value
        timeAlmostUp = (time.clock() - self.prevTime) > (timeLimit - buffer)
        if not grid.canMove():
            return (None, self.Eval(grid), 0)
        
        #if timeAlmostUp:
        #print "time is almost up depth: " + str(depth)
        
        if timeAlmostUp or depth >= 16:
            return (None, self.Heuristic(grid), 0)
        
        #initialize max child and max Value
        (maxChild, maxValue, maxMove) = (None, float('-inf'), 0)
        
        #For each child (one for each possible move), Minimize and save child w/ Max value
        moveOrder = [0, 1, 2, 3]
        for move in moveOrder:
            child = grid.clone()
            isLegalMove = child.move(move)
            if isLegalMove:
                (_, childValue, _) = self.Minimize(child.clone(), alpha, beta, depth + 1)
                if childValue > maxValue:
                    (maxChild, maxValue, maxMove) = (child, childValue, move)
                if maxValue >= beta:
                    break
                if maxValue > alpha:
                    alpha = maxValue
        
        #print "returning maxValue of: " + str(maxValue)
        return (maxChild, maxValue, maxMove)

    def Minimize(self, grid, alpha, beta, depth):
        #If grid state is terminal, return the evaluated grid value
        timeAlmostUp = (time.clock() - self.prevTime) > (timeLimit - buffer)
        if not grid.canMove():
            return (None, self.Eval(grid), 0)
        
        #if timeAlmostUp:
        #print "time is almost up depth: " + str(depth)
        
        if timeAlmostUp or depth >= 8:
            return (None, self.Heuristic(grid), 0)
        
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
                    (_, twoChildValue, _) = self.Maximize(twoChild.clone(), alpha, beta, depth + 1)
                    if twoChildValue < minValue:
                            (minChild, minValue, minMove) = (twoChild, twoChildValue, 0)
                    if minValue <= alpha:
                        break
                    if minValue < beta:
                        beta = minValue
                    
                    #try 4
                    fourChild = grid.clone()
                    fourChild.setCellValue(move, 4)
                    (_, fourChildValue, _) = self.Maximize(fourChild.clone(), alpha, beta, depth + 1)
                    if fourChildValue < minValue:
                        (minChild, minValue, minMove) = (fourChild, fourChildValue, 0)
                    if minValue <= alpha:
                        break
                    if minValue < beta:
                        beta = minValue
                i = i + 1
    
        #print "returning minValue of: " + str(minValue)
        return (minChild, minValue, minMove)

    def Eval(self, grid):
        return grid.getMaxTile()

    def Heuristic(self, grid):
        return len(grid.getAvailableCells())
