import sys
import Queue
import copy
import resource

#Create initial Arcs
def createInitialArcs():
    #formulate all variable which belong in the same constraint
    constraints = []
    #horizontal constraints
    letters =  ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    for l in letters:
        constraints.append([l+'1', l+'2', l+'3', l+'4', l+'5', l+'6', l+'7', l+'8', l+'9'])
    #vertical constraints
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    for n in numbers:
        constraints.append(['A'+n, 'B'+n, 'C'+n, 'D'+n, 'E'+n, 'F'+n, 'G'+n, 'H'+n, 'I'+n])
    #box constraints
    constraints.append(['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'])
    constraints.append(['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3'])
    constraints.append(['G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3'])
    constraints.append(['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6'])
    constraints.append(['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6'])
    constraints.append(['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6'])
    constraints.append(['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'])
    constraints.append(['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9'])
    constraints.append(['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9'])

    #create arcs based on constraints
    arcs = Queue.Queue()
    arcSize = 0
    for c in constraints:
        for i in range(0,9):
            for j in range(0,9):
                if j != i:
                    arcs.put((c[i],c[j]))
    return arcs

#Create initial Board
def createInitialBoard(boardState):
    board = {}
    letters =  ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    i = 0
    for l in letters:
        for n in numbers:
            v = boardState[i]
            if v == '0':
                board[l+n] = (['1','2','3','4','5','6','7','8','9'], False)
            else:
                board[l+n] = ([v], True)
            i = i + 1
    return board

#Create arc neighbors
def createArcNeighbors(arc):
    neighbors = []
    x = list(arc[0])
    xLetter = x[0]
    xNumber = x[1]
    letters =  ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    #add row neighbors
    for n in numbers:
        if xLetter+n != arc[0]:
            neighbors.append((xLetter+n, arc[0]))
    #add column neighbors
    for l in letters:
        if l+xNumber != arc[0]:
            neighbors.append((l+xNumber, arc[0]))

    #add block neighbors
    if xLetter == 'A' or xLetter == 'B' or xLetter == 'C':
        if xNumber == '1' or xNumber == '2' or xNumber =='3':
            for n in ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']:
                if n != arc[0]:
                    neighbors.append((n, arc[0]))
        elif xNumber == '4' or xNumber == '5' or xNumber == '6':
            for n in ['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6']:
                if n != arc[0]:
                    neighbors.append((n, arc[0]))
        else:
            for n in ['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9']:
                if n != arc[0]:
                    neighbors.append((n, arc[0]))
    elif xLetter == 'D' or xLetter == 'E' or xLetter == 'F':
        if xNumber == '1' or xNumber == '2' or xNumber =='3':
            for n in ['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3']:
                if n != arc[0]:
                    neighbors.append((n, arc[0]))
        elif xNumber == '4' or xNumber == '5' or xNumber == '6':
            for n in ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6']:
                if n != arc[0]:
                    neighbors.append((n, arc[0]))
        else:
            for n in ['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9']:
                if n != arc[0]:
                    neighbors.append((n, arc[0]))
    else:
        if xNumber == '1' or xNumber == '2' or xNumber =='3':
            for n in ['G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3']:
                if n != arc[0]:
                    neighbors.append((n, arc[0]))
        elif xNumber == '4' or xNumber == '5' or xNumber == '6':
            for n in ['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6']:
                if n != arc[0]:
                    neighbors.append((n, arc[0]))
        else:
            for n in ['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9']:
                if n != arc[0]:
                    neighbors.append((n, arc[0]))

    return neighbors


#Revise the arc
def revise(arc):
    global board
    revised = False
    domainX = board[arc[0]][0]
    xAlreadySet = board[arc[0]][1]
    domainY = board[arc[1]][0]
    yAlreadySet = board[arc[1]][1]
    if len(domainY) != 1:
        #only revise arcs X->Y when X has not been set yet but Y has
        return revised
    for vX in domainX:
        if vX == domainY[0]:
            #remove vX from domainX, update the board
            domainX.remove(vX)
            board[arc[0]] = (domainX, False)
            revised = True
    return revised

#Perform AC-3 Algorithm
def AC3():
    global board
    global arcs
    while arcs.empty() != True:
        arc = arcs.get()
        if revise(arc):
            if len(board[arc[0]][0]) == 0:
                return False
            arcNeighbors = createArcNeighbors(arc)
            for n in arcNeighbors:
                arcs.put(n)

    for key, value in board.items():
        if len(value[0]) != 1:
            return False
    return True

#determines whether or not an assignment is complete
def isComplete(assignment):
    for key, value in assignment.items():
        if len(value[0]) != 1:
            return False
    return True

#pick next variable to try to assign
#this is based on minimum remaining value
def pickNextVariable(assignment):
    minRemainingCount = 1000
    minRemainingKeyValue = ()
    for key, value in assignment.items():
        alreadyAssigned = value[1]
        if (not alreadyAssigned) and len(value[0]) < minRemainingCount:
            minRemainingCount = len(value[0])
            minRemainingKeyValue = key, value
    return minRemainingKeyValue

#check if assignment is consistent w/ constraints
def isConsistent(d, variableNew, assignment):
    constraintsToCheck = findConstraints(variableNew)

    #for each constraint list, check that no values are equal if they are assigned
    for c in constraintsToCheck:
        #'1'->'A1'
        values = {}
        values[d] = variableNew
        for variable in c:
            alreadyAssigned = assignment[variable][1]
            if variableNew != variable and len(assignment[variable][0]) == 1:
                if assignment[variable][0][0] in values:
                    return False
                values[assignment[variable][0][0]] = variable
    return True

def forwardCheck(assignment, variableNew, d):
    constraintsToCheck = findConstraints(variableNew)
    #for each constraint list, reduce domain where appropriate
    for c in constraintsToCheck:
        for variable in c:
            alreadyAssigned = assignment[variable][1]
            if not alreadyAssigned:
                domain = assignment[variable][0]
                for v in domain:
                    if v == d:
                        domain.remove(v)
                        isAssigned = len(domain) == 1
                        assignment[variable] = (domain, isAssigned)
    return assignment

def findConstraints(variable):
    variableList = list(variable)
    xLetter = variableList[0]
    xNumber = variableList[1]
    constraintsToCheck = []
    letters =  ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    #add row constraint
    rowConstraint = []
    for n in numbers:
        rowConstraint.append(xLetter+n)
    constraintsToCheck.append(rowConstraint)
    #add column constraint
    columnConstraint = []
    for l in letters:
        columnConstraint.append(l+xNumber)
    constraintsToCheck.append(columnConstraint)
    #add block constraint
    blockConstraint = []
    if xLetter == 'A' or xLetter == 'B' or xLetter == 'C':
        if xNumber == '1' or xNumber == '2' or xNumber =='3':
            blockConstraint = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
        elif xNumber == '4' or xNumber == '5' or xNumber == '6':
            blockConstraint = ['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6']
        else:
            blockConstraint = ['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9']
    elif xLetter == 'D' or xLetter == 'E' or xLetter == 'F':
        if xNumber == '1' or xNumber == '2' or xNumber =='3':
            blockConstraint = ['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3']
        elif xNumber == '4' or xNumber == '5' or xNumber == '6':
            blockConstraint = ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6']
        else:
            blockConstraint =  ['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9']
    else:
        if xNumber == '1' or xNumber == '2' or xNumber =='3':
            blockConstraint =  ['G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3']
        elif xNumber == '4' or xNumber == '5' or xNumber == '6':
            blockConstraint =  ['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6']
        else:
            blockConstraint =  ['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9']
    constraintsToCheck.append(blockConstraint)
    return constraintsToCheck

#Perform BTS Algorithm
def BTS(assignment):
    if isComplete(assignment):
        return assignment
    variable, value = pickNextVariable(assignment)
    domain = value[0]
    for d in domain:
        if isConsistent(d, variable, assignment):
            assignmentCopy = copy.deepcopy(assignment)
            assignment[variable] = ([d], True)
            assignment = forwardCheck(assignment, variable, d)
            result = BTS(assignment)
            if result != "failure":
                return result
            assignment = assignmentCopy

    return "failure"

#Create board formatted as a string
def boardToString(board):
    boardString = ''
    letters =  ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    i = 0
    for l in letters:
        for n in numbers:
            boardString = boardString + ((board[l+n])[0])[0]

    return boardString

#Create board formatted as a string
def boardToString2(board):
    boardString = ''
    letters =  ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    i = 0
    for l in letters:
        for n in numbers:
            value = ((board[l+n])[0])[0]
            if len((board[l+n])[0]) != 1:
                value = '0'
            boardString = boardString + value
        boardString = boardString + '\n'

    return boardString

def runInBatch():
    with open("sudokus_start.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    for c in content:
        arcs = createInitialArcs()
        board = createInitialBoard(list(c))
        bts = BTS(copy.deepcopy(board))
        if bts != "failure":
            print "AC3 solved!"
            print boardToString(bts) + ' ' + 'AC3'
        else:
            print "AC3 did not solve"

#python driver.py <input_string>
#runInBatch()
boardArgument = sys.argv[1]
boardState = list(boardArgument)
arcs = createInitialArcs()
board = createInitialBoard(boardState)
boardCopy = copy.deepcopy(board)
if AC3():
    f = open('output.txt', 'w')
    f.write(boardToString(board) + ' ' + 'AC3')
    #print boardToString(board) + ' ' + 'AC3'
else:
    bts = BTS(boardCopy)
    f = open('output.txt', 'w')
    f.write(boardToString(bts) + ' ' + 'BTS')
    #print boardToString(bts) + ' ' + 'BTS'
