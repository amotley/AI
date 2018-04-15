train_path = "../resource/lib/publicdata/aclImdb/train/" # use terminal to ls files under this directory
test_path = "../resource/asnlib/public/imdb_te.csv" # test data for grade evaluation
import pandas as pd
import glob
import csv
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfTransformer

def removeStopWords(stopWords, review):
    removedStopWords = []
    for word in review.split():
        if word.lower() not in stopWords:
            removedStopWords.append(word)
    removedStopWordsText = ' '.join(removedStopWords)
    return removedStopWordsText

def imdb_data_preprocess():
    #read stop words and put into a list
    stopWords = []
    stopWordsFileName = 'stopwords.en.txt'
    with open(stopWordsFileName) as f:
        stopWords = f.read().splitlines()
            #negPath = "neg"
    negPath = train_path + "neg"
    allNegFiles = glob.glob(negPath + "/*.txt")
    #posPath = "pos"
    posPath = train_path + "pos"
    allPosFiles = glob.glob(posPath + "/*.txt")
    trainingCsvName = 'imdb_tr.csv'
    trainingCsv = open(trainingCsvName, "w")
    csvWriter = csv.writer(trainingCsv)
    index = 0
    for file in allPosFiles:
        review = open(file, "r")
        reviewText = review.read()
        toWrite = removeStopWords(stopWords, reviewText)
        csvWriter.writerow([index, toWrite, 1])
        index = index + 1
    for file in allNegFiles:
        review = open(file, "r")
        reviewText = review.read()
        toWrite = removeStopWords(stopWords, reviewText)
        csvWriter.writerow([index, toWrite, 0])
        index = index + 1

if __name__ == "__main__":
    #pre-process the training data
    imdb_data_preprocess()
    filename = 'imdb_tr.csv'
    d = pd.read_csv(filename, encoding = "ISO-8859-1", header=None)
    listOfReviews = d[1].tolist()
    listOfPolarities = d[2].tolist()
    listOfReviewWords = []
    for r in listOfReviews:
        l = []
        for word in re.split("\W+", r):
            l.append(word)
        listOfReviewWords.append(",".join(map(str, l)))
    vector = CountVectorizer()
    data = vector.fit_transform(listOfReviewWords)
    tfidfData = TfidfTransformer(use_idf=True).fit_transform(data)

    #testSetFileName = 'imdb_te.csv'
    testSetFileName = test_path
    d = pd.read_csv(testSetFileName, encoding = "ISO-8859-1")
    listOfTestReviews = d['text'].tolist()
    listOfTestReviewWords = []
    for r in listOfTestReviews:
        l = []
        for word in re.split("\W+", r):
            l.append(word)
        listOfTestReviewWords.append(",".join(map(str, l)))
    testVector = CountVectorizer(vocabulary=vector.vocabulary_)
    testData = testVector.fit_transform(listOfTestReviewWords)
    tfidfTestData = TfidfTransformer(use_idf=True).fit_transform(testData)

    clf = SGDClassifier(loss="hinge", penalty="l1")
    clf.fit(data, listOfPolarities)
    unigramOutputName = 'unigram.output.txt'
    unigramOutput = open(unigramOutputName, "w")
    unigramWriter = csv.writer(unigramOutput)
    for t in testData:
        prediction = clf.predict(t)
        unigramWriter.writerow(prediction)

    clftfidf = SGDClassifier(loss="hinge", penalty="l1")
    clftfidf.fit(tfidfData, listOfPolarities)
    unigramtfidfOutputName = 'unigramtfidf.output.txt'
    unigramtfidfOutput = open(unigramtfidfOutputName, "w")
    unigramtfidfWriter = csv.writer(unigramtfidfOutput)
    for t in tfidfTestData:
        prediction = clf.predict(t)
        unigramtfidfWriter.writerow(prediction)

    #create bigram
    listOfBigrams = []
    for w in listOfReviewWords:
        array = w.split(',')
        bigram = []
        for i in range(len(array)-1):
            bigram.append(array[i] + " " + array[i+1])
        listOfBigrams.append(",".join(bigram))
    bigramVector = CountVectorizer()
    bigramData = bigramVector.fit_transform(listOfBigrams)
    tfidfBigramData = TfidfTransformer(use_idf=True).fit_transform(bigramData)

    listOfTestBigrams = []
    for w in listOfTestReviewWords:
        array = w.split(',')
        bigram = []
        for i in range(len(array)-1):
            bigram.append(array[i] + " " + array[i+1])
        listOfTestBigrams.append(",".join(bigram))
    testBigramVector = CountVectorizer(vocabulary=bigramVector.vocabulary_)
    testBigramData = testBigramVector.fit_transform(listOfTestBigrams)
    tfidfTestBigramData = TfidfTransformer(use_idf=True).fit_transform(testBigramData)

    clfBigram = SGDClassifier(loss="hinge", penalty="l1")
    clfBigram.fit(bigramData, listOfPolarities)
    bigramOutputName = 'bigram.output.txt'
    bigramOutput = open(bigramOutputName, "w")
    bigramWriter = csv.writer(bigramOutput)
    for t in testBigramData:
        prediction = clf.predict(t)
        bigramWriter.writerow(prediction)

    clftfidfBigram = SGDClassifier(loss="hinge", penalty="l1")
    clftfidfBigram.fit(tfidfBigramData, listOfPolarities)
    bigramtfidfOutputName = 'bigramtfidf.output.txt'
    bigramtfidfOutput = open(bigramtfidfOutputName, "w")
    bigramWtfidfWriter = csv.writer(bigramtfidfOutput)
    for t in tfidfTestBigramData:
        prediction = clf.predict(t)
        bigramWtfidfWriter.writerow(prediction)





















