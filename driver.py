import sys
import Queue
import copy
import resource
import time
import heapq

class Board:
    
    hashOfManhattenIndices = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]

    def __init__(self, currentState, zeroIndex):
        self.currentState = copy.deepcopy(currentState)
        self.zeroIndex = copy.deepcopy(zeroIndex)
    
    def isWinner(self):
        return str(self.currentState) == "['0', '1', '2', '3', '4', '5', '6', '7', '8']"
    
    def manhattenDistance(self):
        d = 0
        i = 0
        for block in self.currentState:
            v = int(block)
            if v != 0:
                mdHorizontal = abs(self.hashOfManhattenIndices[i][0] - self.hashOfManhattenIndices[v][0])
                mdVertial = abs(self.hashOfManhattenIndices[i][1] - self.hashOfManhattenIndices[v][1])
                d = d + mdHorizontal + mdVertial
            i = i + 1
        return d

    def moveUp(self):
        if self.zeroIndex < 3:
            return None
        upValue = self.currentState[self.zeroIndex - 3]
        self.currentState[self.zeroIndex] = upValue
        self.currentState[self.zeroIndex - 3] = "0"
        self.zeroIndex = self.zeroIndex - 3
        return self

    def moveDown(self):
        if self.zeroIndex > 5:
            return None
        downValue = self.currentState[self.zeroIndex + 3]
        self.currentState[self.zeroIndex] = downValue
        self.currentState[self.zeroIndex + 3] = "0"
        self.zeroIndex = self.zeroIndex + 3
        return self

    def moveLeft(self):
        if self.zeroIndex == 0 or self.zeroIndex == 3 or self.zeroIndex == 6:
            return None
        leftValue = self.currentState[self.zeroIndex - 1]
        self.currentState[self.zeroIndex] = leftValue
        self.currentState[self.zeroIndex - 1] = "0"
        self.zeroIndex = self.zeroIndex - 1
        return self

    def moveRight(self):
        if self.zeroIndex == 2 or self.zeroIndex == 5 or self.zeroIndex == 8:
            return None
        rightValue = self.currentState[self.zeroIndex + 1]
        self.currentState[self.zeroIndex] = rightValue
        self.currentState[self.zeroIndex + 1] = "0"
        self.zeroIndex = self.zeroIndex + 1
        return self

class Node:
    def __init__(self, board, parent, depth, path):
        self.board = board
        self.parent = parent
        self.depth = depth
        self.path = path

#output to output.txt file
def createOutputFile(path, cost, nodes, depth, maxDepth, runningTime, maxRam):
    pathToGoal = "path_to_goal: " + path
    costOfPath = "cost_of_path: " + str(cost)
    nodesExpanded = "nodes_expanded: " + str(nodes)
    searchDepth = "search_depth: " + str(depth)
    maxSearchDepth = "max_search_depth: " + str(maxDepth)
    runningTime = "running_time: " + str(runningTime)
    maxRamUsage = "max_ram_usage: " + str(maxRam)
    f = open('output.txt', 'w')
    f.write(pathToGoal + "\n")
    f.write(costOfPath + "\n")
    f.write(nodesExpanded + "\n")
    f.write(searchDepth + "\n")
    f.write(maxSearchDepth + "\n")
    f.write(runningTime + "\n")
    f.write(maxRamUsage + "\n")

def bfs(initialBoard):
    #UDLR order
    #Create initial Node
    initialNode = Node(initialBoard, None, 0, "")
    
    #Create Frontier Queue
    frontier = Queue.Queue()
    
    #Create Dictionary to be used to keep track of nodes already visited
    visited = {}
    #add currentNode to 'visited' hash table
    visited[str(initialNode.board.currentState)] = initialNode
    
    #Enqueue the initial Node into the Frontier
    frontier.put(initialNode)
    
    #while frontier is not empty:
    #check for winner
    #else find children in UDLR order and enqueue children
    maxDepth = 0
    nodesExpanded = 0
    while frontier.empty != True:
        currentNode = frontier.get()
        if currentNode.board.isWinner():
            print "winner!"
            print str(currentNode.board.currentState)
            #find the path by traversing up the parents
            path = []
            depthAndCost = currentNode.depth
            runningTime = time.time() - start_time
            ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            while currentNode.parent != None:
                path.insert(0, currentNode.path)
                currentNode = currentNode.parent
            return createOutputFile(str(path), depthAndCost, nodesExpanded, depthAndCost, maxDepth, runningTime, ram)
    
        #add UDLR children to the frontier if they haven't already been visited
        nodesExpanded = nodesExpanded + 1
        currentBoardState = currentNode.board.currentState
        currentBoardZeroIndex = currentNode.board.zeroIndex
        
        upCopy = Board(currentBoardState, currentBoardZeroIndex)
        upChild = upCopy.moveUp()
        if upChild != None:
            if str(upChild.currentState) not in visited:
                if currentNode.depth + 1 > maxDepth:
                    maxDepth = currentNode.depth + 1
                upChildNode = Node(upChild, currentNode, currentNode.depth + 1, "Up")
                frontier.put(upChildNode)
                visited[str(upChild.currentState)] = upChildNode
        
        downCopy = Board(currentBoardState, currentBoardZeroIndex)
        downChild = downCopy.moveDown()
        if downChild != None:
            if str(downChild.currentState) not in visited:
                if currentNode.depth + 1 > maxDepth:
                    maxDepth = currentNode.depth + 1
                downChildNode = Node(downChild, currentNode, currentNode.depth + 1, "Down")
                frontier.put(downChildNode)
                visited[str(downChild.currentState)] = downChildNode
        
        leftCopy = Board(currentBoardState, currentBoardZeroIndex)
        leftChild = leftCopy.moveLeft()
        if leftChild != None:
            if str(leftChild.currentState) not in visited:
                if currentNode.depth + 1 > maxDepth:
                    maxDepth = currentNode.depth + 1
                leftChildNode = Node(leftChild, currentNode, currentNode.depth + 1, "Left")
                frontier.put(leftChildNode)
                visited[str(leftChild.currentState)] = leftChildNode
        
        rightCopy = Board(currentBoardState, currentBoardZeroIndex)
        rightChild = rightCopy.moveRight()
        if rightChild != None:
            if str(rightChild.currentState) not in visited:
                if currentNode.depth + 1 > maxDepth:
                    maxDepth = currentNode.depth + 1
                rightChildNode = Node(rightChild, currentNode, currentNode.depth + 1, "Right")
                frontier.put(rightChildNode)
                visited[str(rightChild.currentState)] = rightChildNode

def dfs(initialBoard):
    #UDLR order
    #Create initial Node
    initialNode = Node(initialBoard, None, 0, "")
    
    #Create Frontier Stack implemented as a list
    frontier = []
    
    #Create Dictionary to be used to keep track of nodes already visited
    visited = {}
    #add currentNode to 'visited' hash table
    visited[str(initialNode.board.currentState)] = initialNode
    
    #Enqueue the initial Node into the Frontier
    frontier.append(initialNode)
    
    #while frontier is not empty:
    #check for winner
    #else find children in UDLR order and enqueue children
    maxDepth = 0
    nodesExpanded = 0
    while len(frontier) != 0:
        currentNode = frontier.pop()
        if currentNode.board.isWinner():
            print "winner!"
            print str(currentNode.board.currentState)
            #find the path by traversing up the parents
            path = []
            depthAndCost = currentNode.depth
            runningTime = time.time() - start_time
            ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            while currentNode.parent != None:
                path.insert(0, currentNode.path)
                currentNode = currentNode.parent
            return createOutputFile(str(path), depthAndCost, nodesExpanded, depthAndCost, maxDepth, runningTime, ram)
        
        #add UDLR children to the frontier if they haven't already been visited
        nodesExpanded = nodesExpanded + 1
        currentBoardState = currentNode.board.currentState
        currentBoardZeroIndex = currentNode.board.zeroIndex
        
        rightCopy = Board(currentBoardState, currentBoardZeroIndex)
        rightChild = rightCopy.moveRight()
        if rightChild != None:
            if str(rightChild.currentState) not in visited:
                if currentNode.depth + 1 > maxDepth:
                    maxDepth = currentNode.depth + 1
                rightChildNode = Node(rightChild, currentNode, currentNode.depth + 1, "Right")
                frontier.append(rightChildNode)
                visited[str(rightChild.currentState)] = rightChildNode


        leftCopy = Board(currentBoardState, currentBoardZeroIndex)
        leftChild = leftCopy.moveLeft()
        if leftChild != None:
            if str(leftChild.currentState) not in visited:
                if currentNode.depth + 1 > maxDepth:
                    maxDepth = currentNode.depth + 1
                leftChildNode = Node(leftChild, currentNode, currentNode.depth + 1, "Left")
                frontier.append(leftChildNode)
                visited[str(leftChild.currentState)] = leftChildNode

        downCopy = Board(currentBoardState, currentBoardZeroIndex)
        downChild = downCopy.moveDown()
        if downChild != None:
            if str(downChild.currentState) not in visited:
                if currentNode.depth + 1 > maxDepth:
                    maxDepth = currentNode.depth + 1
                downChildNode = Node(downChild, currentNode, currentNode.depth + 1, "Down")
                frontier.append(downChildNode)
                visited[str(downChild.currentState)] = downChildNode

        upCopy = Board(currentBoardState, currentBoardZeroIndex)
        upChild = upCopy.moveUp()
        if upChild != None:
            if str(upChild.currentState) not in visited:
                if currentNode.depth + 1 > maxDepth:
                    maxDepth = currentNode.depth + 1
                upChildNode = Node(upChild, currentNode, currentNode.depth + 1, "Up")
                frontier.append(upChildNode)
                visited[str(upChild.currentState)] = upChildNode

def ast(initialBoard):
    #Create initial Node
    initialNode = Node(initialBoard, None, 0, "")
    initialNodeHeuristic = initialBoard.manhattenDistance()
    
    #Create Frontier Priority Queue
    frontier = []
    
    #Create Dictionary to be used to keep track of nodes already visited
    visited = {}
    #add currentNode and its heuristic value (Manhatten distance) to 'visited' hash table
    visited[str(initialNode.board.currentState)] = (initialNodeHeuristic, initialNode)
    
    #Push the initial Node into the Frontier
    heapq.heappush(frontier, (initialNodeHeuristic, initialNode))
    
    #while frontier is not empty:
    #check for winner
    #else find children in UDLR order and push children
    maxDepth = 0
    nodesExpanded = 0
    while len(frontier) != 0:
        currentNodeTuple = heapq.heappop(frontier)
        currentNode = currentNodeTuple[1]
        if currentNode.board.isWinner():
            print "winner!"
            print str(currentNode.board.currentState)
            #find the path by traversing up the parents
            path = []
            depthAndCost = currentNode.depth
            runningTime = time.time() - start_time
            ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            while currentNode.parent != None:
                path.insert(0, currentNode.path)
                currentNode = currentNode.parent
            return createOutputFile(str(path), depthAndCost, nodesExpanded, depthAndCost, maxDepth, runningTime, ram)
        
        #add UDLR children to the frontier if they haven't already been visited
        nodesExpanded = nodesExpanded + 1
        currentBoardState = currentNode.board.currentState
        currentBoardZeroIndex = currentNode.board.zeroIndex

        rightCopy = Board(currentBoardState, currentBoardZeroIndex)
        rightChild = rightCopy.moveRight()
        if rightChild != None:
            rightChildHeuristic = rightChild.manhattenDistance() + currentNode.depth + 1
            if str(rightChild.currentState) not in visited:
                if currentNode.depth + 1 > maxDepth:
                    maxDepth = currentNode.depth + 1
                rightChildNode = Node(rightChild, currentNode, currentNode.depth + 1, "Right")
                heapq.heappush(frontier, (rightChildHeuristic, rightChildNode))
                visited[str(rightChild.currentState)] = (rightChildHeuristic, rightChildNode)

        leftCopy = Board(currentBoardState, currentBoardZeroIndex)
        leftChild = leftCopy.moveLeft()
        if leftChild != None:
            leftChildHeuristic = leftChild.manhattenDistance() + currentNode.depth + 1
            if str(leftChild.currentState) not in visited:
                if currentNode.depth + 1 > maxDepth:
                    maxDepth = currentNode.depth + 1
                leftChildNode = Node(leftChild, currentNode, currentNode.depth + 1, "Left")
                heapq.heappush(frontier, (leftChildHeuristic, leftChildNode))
                visited[str(leftChild.currentState)] = (leftChildHeuristic, leftChildNode)

        downCopy = Board(currentBoardState, currentBoardZeroIndex)
        downChild = downCopy.moveDown()
        if downChild != None:
            downChildHeuristic = downChild.manhattenDistance() + currentNode.depth + 1
            if str(downChild.currentState) not in visited:
                if currentNode.depth + 1 > maxDepth:
                    maxDepth = currentNode.depth + 1
                downChildNode = Node(downChild, currentNode, currentNode.depth + 1, "Down")
                heapq.heappush(frontier, (downChildHeuristic, downChildNode))
                visited[str(downChild.currentState)] = (downChildHeuristic, downChildNode)

        upCopy = Board(currentBoardState, currentBoardZeroIndex)
        upChild = upCopy.moveUp()
        if upChild != None:
            upChildHeuristic = upChild.manhattenDistance() + currentNode.depth + 1
            if str(upChild.currentState) not in visited:
                if currentNode.depth + 1 > maxDepth:
                    maxDepth = currentNode.depth + 1
                upChildNode = Node(upChild, currentNode, currentNode.depth + 1, "Up")
                heapq.heappush(frontier, (upChildHeuristic, upChildNode))
                visited[str(upChild.currentState)] = (upChildHeuristic, upChildNode)
    




#python driver.py bfs 0,8,7,6,5,4,3,2,1
#terminal
start_time = time.time()
actionNameArgument = sys.argv[1]
boardArgument = sys.argv[2]
currentState = boardArgument.split(",")
zeroIndex = currentState.index("0")
board = Board(currentState, zeroIndex)
if actionNameArgument == "bfs":
    bfs(board)
elif actionNameArgument == "dfs":
    dfs(board)
elif actionNameArgument == "ast":
    ast(board)
else:
    print "invalid arguments"

