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
            return (None, self.Heuristic(grid), 0)
        
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
    
        return (maxChild, maxValue, maxMove)

    def Minimize(self, grid, alpha, beta, depth):
        #If grid state is terminal, return the evaluated grid value
        timeAlmostUp = (time.clock() - self.prevTime) > (timeLimit - buffer)
        if not grid.canMove():
            return (None, self.Heuristic(grid), 0)
        
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
    
        return (minChild, minValue, minMove)

    def Eval(self, grid):
        return grid.getMaxTile()

    def Heuristic(self, grid):
        maxTileBonus = 0
        if grid.getMaxTile() >= 1024:
            maxTileBonus = grid.getMaxTile()
        return self.CalculateMonotonicity(grid)*28 - self.CalculateEmptyCellPenalty(grid)*28 + maxTileBonus

    def CalculateEmptyCellPenalty(self, grid):
        if len(grid.getAvailableCells()) < 4:
            return 4
        return 0

    def CalculateMonotonicity(self, grid):
        #For each row (left->right) and col(up->down)
        #calculate number of tiles in increasing order, and decreasing order
        #assign score for each row, col based on max (numIncreasing, numDecreasing)
        matrix = grid.map
        row = 0
        totalPoints = 0
        totalPointsDecreasingRows = 0
        totalPointsIncreasingRows = 0
        totalPointsDecreasingCols = 0
        totalPointsIncreasingCols = 0
        while row < 4:
            numIncreasingRow = 0
            numDecreasingRow = 0
            numIncreasingCol = 0
            numDecreasingCol = 0
            col = 0
            prevRow = matrix[row][col]
            prevCol = matrix[col][row]
            while col < 3:
                if matrix[row][col + 1] <= prevRow:
                    numDecreasingRow = numDecreasingRow + 1
                    #extra point if the tiles are the same (and not 0)
                    if matrix[row][col + 1] == prevRow and matrix[row][col + 1] != 0:
                        numDecreasingRow = numDecreasingRow + 1
                if matrix[row][col + 1] >= prevRow:
                    numIncreasingRow = numIncreasingRow + 1
                        #extra point if the tiles are the same (and not 0)
                    if matrix[row][col + 1] == prevRow and matrix[row][col + 1] != 0:
                        numIncreasingRow = numIncreasingRow + 1
                if matrix[col + 1][row] <= prevCol:
                    numDecreasingCol = numDecreasingCol + 1
                    #extra point if the tiles are the same (and not 0)
                    if matrix[col + 1][row] == prevCol and matrix[col + 1][row] != 0:
                        numDecreasingCol = numDecreasingCol + 1
                if matrix[col + 1][row] >= prevCol:
                    numIncreasingCol = numIncreasingCol + 1
                    #extra point if the tiles are the same (and not 0)
                    if matrix[col + 1][row] == prevCol and matrix[col + 1][row] != 0:
                        numIncreasingCol = numIncreasingCol + 1
                prevRow = matrix[row][col + 1]
                prevCol = matrix[col + 1][row]
                col = col + 1
            totalPointsDecreasingRows = totalPointsDecreasingRows + numDecreasingRow
            totalPointsIncreasingRows = totalPointsIncreasingRows + numIncreasingRow
            totalPointsDecreasingCols = totalPointsDecreasingCols + numDecreasingCol
            totalPointsIncreasingCols = totalPointsIncreasingCols + numIncreasingCol
            row = row + 1
        totalPoints = max(totalPointsDecreasingRows + totalPointsDecreasingCols, totalPointsIncreasingRows + totalPointsIncreasingCols)
        #print "totalPoints" + str(totalPoints)
        return totalPoints

    def CalculateSmoothness(self, grid):
        return 0

