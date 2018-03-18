import sys
import csv
import matplotlib
#import matplotlib.pyplot as plt
#import numpy as np

#Data class
class Data:
    def __init__(self, x1, x2, y):
        self.x1 = x1
        self.x2 = x2
        self.y = y

#calculateOutput
def calculateOutput(x1, x2):
    global w1
    global w2
    global b
    sum = b + w1*x1 + w2*x2
    if sum > 0:
        return 1
    else:
        return -1

#calculateError
def calculateError(output, xValue, y):
    if output == y:
        return 0
    elif output > y:
        return -1
    elif output < y:
        return 1

#calculateNewWeight
def adjustWeights(x1, x2, y):
    global w1
    global w2
    global b
    global learningRate
    error = calculateError(calculateOutput(x1, x2), x1, y)
    w1 = w1 + learningRate*x1*error
    w2 = w2 + learningRate*x2*error
    b = b + learningRate*error

#python problem1.py input1.csv output1.csv
#read input and initialize data
inputArgument = sys.argv[1]
outputArgument = sys.argv[2]
dataList = []
dataSize = 0
learningRate = .2
w1 = 0
w2 = 0
b = 0
with open(inputArgument) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        d = Data(float(row[0]),float(row[1]),float(row[2]))
        dataList.append(d)
        dataSize = dataSize + 1

#until convergence, train weights
w1_old = 100
w2_old = 100
b_old = 100
while ((abs(w1_old - w1) > 0.0005) or (abs(w2_old - w2) > 0.0005) or (abs(b_old - b) > 0.0005)):
    w1_old = w1
    w2_old = w2
    b_old = b
    for d in dataList:
        adjustWeights(d.x1, d.x2, d.y)
    with open(outputArgument, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([w1,w2,b])
#for d in dataList:
#   color = 'r'
#   if d.y == -1:
#       color = 'b'
#   plt.plot(d.x1,d.x2, 'ro',color = color)
#x1 = np.linspace(0,16,30)
#x2 = np.linspace(0,16,30)
#plt.plot(x2,(-b-w1*x1)/w2)
#plt.show()
#print w1, w2, b




