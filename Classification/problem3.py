import sys
import csv
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
#import matplotlib
#import matplotlib.pyplot as plt
#import numpy as np

#python problem3.py input3.csv output3.csv
#read input and initialize data into X and Y lists
inputArgument = sys.argv[1]
outputArgument = sys.argv[2]
xList = []
yList = []
with open(inputArgument) as csvfile:
    reader = csv.reader(csvfile.read().splitlines())
    i = 0
    for row in reader:
        #skip first row
        if i != 0:
            xList.append([float(row[0]), float(row[1])])
            yList.append(float(row[2]))
        i = i + 1

#split data into training(60%) and testing(40%) sets
x_train, x_test, y_train, y_test = train_test_split(xList, yList,test_size=0.40,stratify=yList)


# Set the parameters by cross-validation
linear_parameters = [{'kernel': ['linear'], 'C': [0.1, 0.5, 1.0, 5.0, 10.0, 50.0, 100.0]}]
polynomial_parameters = [{'kernel': ['poly'], 'gamma': [0.1,0.5],'C': [0.1,1.0,3.0],'degree':[4,5,6]}]
rbf_parameters = [{'kernel': ['rbf'], 'gamma': [0.1,0.5,1.0,3.0,6.0,10.0],'C': [0.1,0.5,1.0,5.0,10.0,50.0,100.0]}]
logisticRegression_parameter = [{'C': [0.1,0.5,1.0,5.0,10.0,50.0,100.0]}]
n_neighbors = []
for i in range(1, 51):
    n_neighbors.append(i)
leaf_size = []
for i in range(5, 65, 5):
    leaf_size.append(i)
nearestNeighbors_parameters = [{'n_neighbors': n_neighbors, 'leaf_size': leaf_size}]
tree_parameters = [{'max_depth': n_neighbors, 'min_samples_split': [2,3,4,5,6,7,8,9,10]}]
clf = GridSearchCV(svm.SVC(),polynomial_parameters, cv=5)
#clf = GridSearchCV(linear_model.LogisticRegression(), logisticRegression_parameter, cv=5)
#clf = GridSearchCV(KNeighborsClassifier(), nearestNeighbors_parameters, cv=5)
#clf = GridSearchCV(tree.DecisionTreeClassifier(), tree_parameters, cv=5)
#clf = GridSearchCV(RandomForestClassifier(), tree_parameters, cv=5)
clf.fit(x_train, y_train)
print(clf.best_params_)
print
means = clf.cv_results_['mean_test_score']
stds = clf.cv_results_['std_test_score']
for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
print
#y_true, y_pred = y_test, clf.predict(x_test)
#print(classification_report(y_true, y_pred))
print clf.score(x_test, y_test)

#train the "training" data set using kfold=5 method, and obtain the "best score"
#clf = svm.SVC(kernel='linear', C=100.0)
#clf.fit(x_train, y_train)
#scores = cross_val_score(clf, x_train, y_train, cv=5)
#bestScore = scores.mean()
#print scores
#print "bestScore: " + str(bestScore)
#refit data after cross validation
#clf.fit(x_train, y_train)


#obtain test score from the "testing" set
#testScore = clf.score(x_test, y_test)
#print "testScore: " + str(testScore)
#predicated = cross_val_predict(clf, x_test, y_test, cv=5)
#accuracy = metrics.accuracy_score(y_test, predicated)
#print accuracy

#with open(outputArgument, 'a') as csvfile:
# writer = csv.writer(csvfile)
#writer.writerow([r, 100, b_0, b_age, b_weight])





