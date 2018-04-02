import sys
import csv
#import matplotlib
#import matplotlib.pyplot as plt
#import numpy as np

#Data class
class Data:
    def __init__(self, age, weight, height):
        self.age = age
        self.weight = weight
        self.height = height

#python problem2.py input2.csv output2.csv
#read input and initialize data
inputArgument = sys.argv[1]
outputArgument = sys.argv[2]
dataList = []
dataSize = 0.0
sumAge = 0.0
sumWeight = 0.0
with open(inputArgument) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        d = Data(float(row[0]),float(row[1]),float(row[2]))
        dataList.append(d)
        dataSize = dataSize + 1.0
        sumAge = sumAge + float(row[0])
        sumWeight = sumWeight + float(row[1])

meanAge = sumAge/dataSize
meanWeight = sumWeight/dataSize
sumAgeSquared = 0.0
sumWeightSquared = 0.0
for d in dataList:
    sumAgeSquared = sumAgeSquared + (float(d.age) - meanAge)**2
    sumWeightSquared = sumWeightSquared + (float(d.weight) - meanWeight)**2

#normalize the data
normalizedDataList = []
populationStandardDeviation_age = ((sumAgeSquared)/dataSize)**(.5)
populationStandardDeviation_weight = ((sumWeightSquared)/dataSize)**(.5)
for d in dataList:
    d = Data((d.age-meanAge)/populationStandardDeviation_age, (d.weight-meanWeight)/populationStandardDeviation_weight, d.height)
    print d.age, d.weight, d.height
    normalizedDataList.append(d)

#try out the different learning rates
learningRates = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 1.15]
for r in learningRates:
    i = 0
    b_0 = 0.0
    b_age = 0.0
    b_weight = 0.0
    while (i < 100):
        b_0_sum = 0.0
        b_age_sum = 0.0
        b_weight_sum = 0.0
        for d in normalizedDataList:
            predictionDiff = (b_0 + b_age*d.age + b_weight*d.weight) - d.height
            b_0_sum = b_0_sum + predictionDiff
            b_age_sum = b_age_sum + predictionDiff*d.age
            b_weight_sum = b_weight_sum + predictionDiff*d.weight
        b_0 = b_0 - ((r/dataSize)*b_0_sum)
        b_age = b_age - ((r/dataSize)*b_age_sum)
        b_weight = b_weight - ((r/dataSize)*b_weight_sum)
        i = i + 1

    with open(outputArgument, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([r, 100, b_0, b_age, b_weight])
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




