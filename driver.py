import sys
import Queue
import copy
import resource
import time
import heapq

#Direction Enum
class Direction:
    Up = "Up"
    Down = "Down"
    Left = "Left"
    Right = "Right"

#Node class
class Node:
    def __init__(self, board, parent, depth, path):
        self.board = board
        self.parent = parent
        self.depth = depth
        self.path = path

#Board class
class Board:
    
    hashOfManhattenIndices = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]

    def __init__(self, currentState, zeroIndex):
        self.currentState = currentState[:]
        self.zeroIndex = zeroIndex
    
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
            
    def move(self, direction):
        swapIndex = 0
        if direction == Direction.Up:
            swapIndex = self.zeroIndex - 3
            if self.zeroIndex < 3:
                return None
        elif direction == Direction.Down:
            swapIndex = self.zeroIndex + 3
            if self.zeroIndex > 5:
                return None
        elif direction == Direction.Left:
            swapIndex = self.zeroIndex - 1
            if self.zeroIndex == 0 or self.zeroIndex == 3 or self.zeroIndex == 6:
                return None
        elif direction == Direction.Right:
            swapIndex = self.zeroIndex + 1
            if self.zeroIndex == 2 or self.zeroIndex == 5 or self.zeroIndex == 8:
                return None
        swapValue = self.currentState[swapIndex]
        self.currentState[self.zeroIndex] = swapValue
        self.currentState[swapIndex] = "0"
        self.zeroIndex = swapIndex
        return self

def bfs(initialBoard):
    #Initialize frontier queue and visited dictionary
    initialNode = Node(initialBoard, None, 0, "")
    frontier = Queue.Queue()
    frontier.put(initialNode)
    visited = {}
    visited[str(initialNode.board.currentState)] = initialNode
    maxDepth = [0]
    nodesExpanded = 0
    
    #while frontier is not empty, check and expand
    while frontier.empty != True:
        #get Node from the frontier
        currentNode = frontier.get()
        
        #check if Node is a winner
        if checkWinner(currentNode, nodesExpanded, maxDepth[0]):
            return
    
        #add UDLR children to the frontier if they haven't already been visited
        nodesExpanded = nodesExpanded + 1
        directionOrder = [Direction.Up, Direction.Down, Direction.Left, Direction.Right]
        for direction in directionOrder:
            addChild("bfs", direction, frontier, visited, currentNode, maxDepth)

def dfs(initialBoard):
    #Initialize frontier stack and visited dictionary
    initialNode = Node(initialBoard, None, 0, "")
    frontier = []
    frontier.append(initialNode)
    visited = {}
    visited[str(initialNode.board.currentState)] = initialNode
    maxDepth = [0]
    nodesExpanded = 0
    
    #while frontier is not empty, check and expand
    while len(frontier) != 0:
        currentNode = frontier.pop()
        
        #check if Node is a winner
        if checkWinner(currentNode, nodesExpanded, maxDepth[0]):
            return
        
        #add RLDU children to the frontier if they haven't already been visited
        nodesExpanded = nodesExpanded + 1
        directionOrder = [Direction.Right, Direction.Left, Direction.Down, Direction.Up]
        for direction in directionOrder:
            addChild("dfs", direction, frontier, visited, currentNode, maxDepth)

def ast(initialBoard):
    #Initialize frontier priority queue and visited dictionary
    initialNode = Node(initialBoard, None, 0, "")
    initialNodeHeuristic = initialBoard.manhattenDistance()
    frontier = []
    heapq.heappush(frontier, (initialNodeHeuristic, initialNode))
    visited = {}
    visited[str(initialNode.board.currentState)] = initialNode
    maxDepth = [0]
    nodesExpanded = 0
    
    #while frontier is not empty:
    #check for winner
    #else find children in UDLR order and push children
    while len(frontier) != 0:
        currentNodeTuple = heapq.heappop(frontier)
        currentNode = currentNodeTuple[1]
        
        #check if Node is a winner
        if checkWinner(currentNode, nodesExpanded, maxDepth[0]):
            return
        
        #add UDLR children to the frontier if they haven't already been visited
        nodesExpanded = nodesExpanded + 1
        directionOrder = [Direction.Up, Direction.Down, Direction.Left, Direction.Right]
        for direction in directionOrder:
            addChild("ast", direction, frontier, visited, currentNode, maxDepth)

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

#check whether a node is a winner
def checkWinner(currentNode, nodesExpanded, maxDepth):
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
        createOutputFile(str(path), depthAndCost, nodesExpanded, depthAndCost, maxDepth, runningTime, ram)
        return True
    return False

#Add a child to a search tree
def addChild(searchType, childType, frontier, visited, currentNode, maxDepth):
    currentBoardState = currentNode.board.currentState
    currentBoardZeroIndex = currentNode.board.zeroIndex
    copy = Board(currentBoardState, currentBoardZeroIndex)
    child = copy.move(childType)
    if child != None:
        if str(child.currentState) not in visited:
            if currentNode.depth + 1 > maxDepth[0]:
                maxDepth[0] = currentNode.depth + 1
            childNode = Node(child, currentNode, currentNode.depth + 1, childType)
            if searchType == "bfs":
                #frontier is a queue
                frontier.put(childNode)
            elif searchType == "dfs":
                #frontier is a stack
                frontier.append(childNode)
            elif searchType == "ast":
                #frontier is a priority queue
                childPriority = child.manhattenDistance() + currentNode.depth + 1
                heapq.heappush(frontier, (childPriority, childNode))
            visited[str(child.currentState)] = childNode

#python driver.py bfs 0,8,7,6,5,4,3,2,1
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
