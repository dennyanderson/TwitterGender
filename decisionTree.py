from id3 import Id3Estimator
from id3 import export_graphviz
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
import scipy.stats as st
from os import system

# class to encode multiple columns
class MultiColumnLabelEncoder:
    def __init__(self,columns = None):
        self.columns = columns # array of column names to encode

    def fit(self,X,y=None):
        return self # not relevant here

    # transforms columns of X specified in self.columns using LabelEncoder()
    # if no columns specified, transforms all columns in X
    def transform(self,X):
        output = X.copy()
        if self.columns is not None:
            for col in self.columns:
                output[col] = preprocessing.LabelEncoder().fit_transform(output[col])
        else:
            for colname,col in output.iteritems():
                output[colname] = preprocessing.LabelEncoder().fit_transform(col)
        return output

    def fit_transform(self,X,y=None):
        return self.fit(X,y).transform(X)

# data column names
names = ['fav_number', 'link_color', 'retweet_count', 'sidebar_color', 'tweet_count', 'gender']
# read in the data
gender_data = pd.read_csv('genderCSVedit.csv', header=None, names=names)
# wrap in dataframe
gender_df = pd.DataFrame(gender_data)

# create transformed data frame
# insert the names of the columns that must be encoded as strings
transformed = MultiColumnLabelEncoder(
    columns = ['link_color', 'sidebar_color', 'gender']).fit_transform(gender_df)

# slice the transformed dataframe into an array
data = np.array(transformed.ix[:, :5])
# identify the target
target = np.array(transformed['gender'])

estimator = Id3Estimator()
estimator.fit(data, target)
export_graphviz(estimator.tree_, 'gender_tree.dot', names)

fold_one = 4708
fold_two = 9417
fold_three = 14126
fold_four = 18835

dataOne = data[4709:18836]
dataTwo = np.append(data[0:4709], data[9417:18836], axis=0)
dataThree = np.append(data[0:9417], data[14127:18836], axis=0)
dataFour = data[0:14127]

targetOne = target[4709:18836]
targetTwo = np.append(target[0:4709], target[9417:18836], axis=0)
targetThree = np.append(target[0:9417], target[14127:18836], axis=0)
targetFour = target[0:14127]

estimator1 = Id3Estimator()
estimator2 = Id3Estimator()
estimator3 = Id3Estimator()
estimator4 = Id3Estimator()

dataTone = data[0:4709]
dataTtwo = data[4709:9417]
dataTthree = data[9417:14127]
dataTfour = data[14127:18836]

targetTone = target[0:4709]
targetTtwo = target[4709:9417]
targetTthree = target[9417:14127]
targetTfour = target[14127:18836]

estimator1.fit(dataOne, targetOne)
estimator2.fit(dataTwo, targetTwo)
estimator3.fit(dataThree, targetThree)
estimator4.fit(dataFour, targetFour)

confused1 = confusion_matrix(targetTone, estimator1.predict(dataTone)) # 0.51731
confused2 = confusion_matrix(targetTtwo, estimator2.predict(dataTtwo)) # 0.51327
confused3 = confusion_matrix(targetTthree, estimator3.predict(dataTthree)) # 0.50563
confused4 = confusion_matrix(targetTfour, estimator4.predict(dataTfour)) # 0.51412
    
export_graphviz(estimator1.tree_, 'gender_cval_1.dot', names)

confusionMatrix = confused1

print ('confused1: ' + str(confused1))
print ('confused2: ' + str(confused2))
print ('confused3: ' + str(confused3))
print ('confused4: ' + str(confused4))

#command = ["dot", "-Tpng", "tree.dot", "-o", "tree.png"]
#try:
#    subprocess.check_call(command)
#except:
#    exit("Could not run dot, ie graphviz, to produce visualization")

#from subprocess import check_call
#check_call(['dot','-Tpng','tree.dot','-o','tree.png'])

#system("dot -Tpng gender_tree.dot > gender_tree.png")

correct1 = 0
incorrect1 = 0
correct2 = 0
incorrect2 = 0
correct3 = 0
incorrect3 = 0
correct4 = 0
incorrect4 = 0
correct5 = 0
incorrect5 = 0
correct6 = 0
incorrect6 = 0
correct7 = 0
incorrect7 = 0
correct8 = 0
incorrect8 = 0
correct9 = 0
incorrect9 = 0
correct10 = 0
incorrect10 = 0
correct11 = 0
incorrect11 = 0
correct12 = 0
incorrect12 = 0
correct13 = 0
incorrect13 = 0
correct14 = 0
incorrect14 = 0
correct15 = 0
incorrect15 = 0
correct16 = 0
incorrect16 = 0
correct17 = 0
incorrect17 = 0
correct18 = 0
incorrect18 = 0
correct19 = 0
incorrect19 = 0
index = 0
while (index < 18836):
    if (data[index][0] <= 26.5): # fav_number
        if (data[index][4] <= 31102.5): # tweet_count
            if (data[index][3] <= 8.5): # sidebar_color
                if (data[index][1] <= 7.5): # link_color
                    if (data[index][2] <= 0.5): # retweet_count
                        if (target[index] == 0): # brand
                            correct1 = correct1 + 1
                        else:
                            incorrect1 = incorrect1 + 1
                    if (data[index][2] > 0.5): # retweet_count
                        if (target[index] == 2): # male
                            correct2 = correct2 + 1
                        else:
                            incorrect2 = incorrect2 + 1
                if (data[index][1] > 7.5): # link_color
                    if (target[index] == 0): # brand
                        correct3 = correct3 + 1
                    else:
                        incorrect3 = incorrect3 + 1
            if (data[index][3] > 8.5): # sidebar_color
                if (data[index][1] <= 6): # link_color
                    if (target[index] == 0): # brand
                        correct4 = correct4 + 1
                    else:
                        incorrect4 = incorrect4 + 1
                if (data[index][1] > 6): # link_color
                    if (data[index][2] <= 6.5): # retweet_count
                        if (target[index] == 0): # brand
                            correct5 = correct5 + 1
                        else:
                            incorrect5 = incorrect5 + 1
                    if (data[index][2] > 6.5): # retweet_count
                        if (target[index] == 2): # male
                            correct6 = correct6 + 1
                        else:
                            incorrect6 = incorrect6 + 1
        if (data[index][4] > 31102.5): # tweet_count
            if (data[index][1] <= 2.5): # link_color
                if (target[index] == 0): # brand
                    correct7 = correct7 + 1
                else:
                    incorrect7 = incorrect7 + 1
            if (data[index][1] > 2.5): # link_color
                if (data[index][3] <= 11.5): # sidebar_color
                    if (target[index] == 0): # brand
                        correct8 = correct8 + 1
                    else:
                        incorrect8 = incorrect8 + 1
                if (data[index][3] > 11.5): # sidebar_color
                    if (data[index][2] <= 0.5): # retweet_count
                        if (target[index] == 0): # brand
                            correct9 = correct9 + 1
                        else:
                            incorrect9 = incorrect9 + 1
                    if (data[index][2] > 0.5): # retweet_count
                        if (target[index] == 2): # male
                            correct10 = correct10 + 1
                        else:
                            incorrect10 = incorrect10 + 1
    if (data[index][0] > 26.5): # fav_number
        if (data[index][1] <= 11.5): # link_color
            if (data[index][4] <= 2113): # tweet_count
                if (data[index][2] <= 0.5): # retweet_count
                    if (target[index] == 1): # female
                        correct11 = correct11 + 1
                    else:
                        incorrect11 = incorrect11 + 1
                if (data[index][2] > 0.5): # retweet_count
                    if (target[index] == 0): # brand
                        correct12 = correct12 + 1
                    else:
                        incorrect12 = incorrect12 + 1
            if (data[index][4] > 2113): # tweet_count
                if (data[index][3] <= 1.5): # sidebar_color
                    if (data[index][2] <= 11.5): # retweet_count
                        if (target[index] == 1): # female
                            correct13 = correct13 + 1
                        else:
                            incorrect13 = incorrect13 + 1
                    if (data[index][2] > 11.5): # retweet_count
                        if (target[index] == 0): # brand
                            correct14 = correct14 + 1
                        else:
                            incorrect14 = incorrect14 + 1
                if (data[index][3] > 1.5): # sidebar_color
                    if (target[index] == 1): # female
                        correct15 = correct15 + 1
                    else:
                        incorrect15 = incorrect15 + 1
        if (data[index][1] > 11.5): # link_color
            if (data[index][4] <= 41891): # tweet_count
                if (data[index][3] <= 11.5): # sidebar_color
                    if (target[index] == 2): # male
                        correct16 = correct16 + 1
                    else:
                        incorrect16 = incorrect16 + 1
                if (data[index][3] > 11.5): # sidebar_color
                    if (data[index][2] <= 0.5): # retweet_count
                        if (target[index] == 2): # male
                            correct17 = correct17 + 1
                        else:
                            incorrect17 = incorrect17 + 1
                    if (data[index][2] > 0.5): # retweet_count
                        if (target[index] == 0): # brand
                            correct18 = correct18 + 1
                        else:
                            incorrect18 = incorrect18 + 1
            if (data[index][4] > 41891): # tweet_count
                if (target[index] == 2): # male
                    correct19 = correct19 + 1
                else:
                    incorrect19 = incorrect19 + 1
    index = index + 1

#print (correct1)
#print (incorrect1)
#print (correct2)
#print (incorrect2)
#print (correct3)
#print (incorrect3)
#print (correct4)
#print (incorrect4)
#print (correct5)
#print (incorrect5)
#print (correct6)
#print (incorrect6)
#print (correct7)
#print (incorrect7)
#print (correct8)
#print (incorrect8)
#print (correct9)
#print (incorrect9)
#print (correct10)
#print (incorrect10)
#print (correct11)
#print (incorrect11)
#print (correct12)
#print (incorrect12)
#print (correct13)
#print (incorrect13)
#print (correct14)
#print (incorrect14)
#print (correct15)
#print (incorrect15)
#print (correct16)
#print (incorrect16)
#print (correct17)
#print (incorrect17)
#print (correct18)
#print (incorrect18)
#print (correct19)
#print (incorrect19)

correctBrand = 53+289+6+61+3+959+17+2+1807+5+195+7+4+2+26+28
incorrectBrand = 84+211+1+59+0+1110+13+0+408+2+66+8+2+1+39+11
correctFemale = 386+5+982+1581+44
incorrectFemale = 449+1+1102+1332+77
correctMale = 2+1+2+2193+79+466+55+438+3+3
incorrectMale = 1+0+2+2732+88+680+93+559+0+1

print ("correctBrand: " + str(correctBrand))
print ("incorrectBrand: " + str(incorrectBrand))
print ("correctFemale: " + str(correctFemale))
print ("incorrectFemale: " + str(incorrectFemale))
print ("correctMale: " + str(correctMale))
print ("incorrectMale: " + str(incorrectMale))

print ("confusionMatrix:\n" + str(confusionMatrix))
print ("brand classified as brand: " + str(confusionMatrix[0][0]))
print ("female classified as female: " + str(confusionMatrix[1][1]))
print ("male classified as male: " + str(confusionMatrix[2][2]))
print ("brand classified as female: " + str(confusionMatrix[0][1]))
print ("brand classified as male: " + str(confusionMatrix[0][2]))
print ("female classified as brand: " + str(confusionMatrix[1][0]))
print ("female classified as male: " + str(confusionMatrix[1][2]))
print ("male classified as brand: " + str(confusionMatrix[2][0]))
print ("male classified as female: " + str(confusionMatrix[2][1]))

truePositiveBrand = confusionMatrix[0][0]
falsePositiveBrand = confusionMatrix[1][0] + confusionMatrix[2][0]
trueNegativeBrand = confusionMatrix[1][1] + confusionMatrix[2][2] + confusionMatrix[1][2] + confusionMatrix[2][1]
falseNegativeBrand = confusionMatrix[0][1] + confusionMatrix[0][2]
truePositiveFemale = confusionMatrix[1][1]
falsePositiveFemale = confusionMatrix[0][1] + confusionMatrix[2][1]
trueNegativeFemale = confusionMatrix[0][0] + confusionMatrix[2][2] + confusionMatrix[0][2] + confusionMatrix[2][0]
falseNegativeFemale = confusionMatrix[1][0] + confusionMatrix[1][2]
truePositiveMale = confusionMatrix[2][2]
falsePositiveMale = confusionMatrix[0][2] + confusionMatrix[1][2]
trueNegativeMale = confusionMatrix[0][0] + confusionMatrix[1][1] + confusionMatrix[0][1] + confusionMatrix[1][0]
falseNegativeMale = confusionMatrix[2][0] + confusionMatrix[2][1]

print ("truePositiveBrand: " + str(truePositiveBrand))
print ("falsePositiveBrand: " + str(falsePositiveBrand))
print ("trueNegativeBrand: " + str(trueNegativeBrand))
print ("falseNegativeBrand: " + str(falseNegativeBrand))
print ("truePositiveFemale: " + str(truePositiveFemale))
print ("falsePositiveFemale: " + str(falsePositiveFemale))
print ("trueNegativeFemale: " + str(trueNegativeFemale))
print ("falseNegativeFemale: " + str(falseNegativeFemale))
print ("truePositiveMale: " + str(truePositiveMale))
print ("falsePositiveMale: " + str(falsePositiveMale))
print ("trueNegativeMale: " + str(trueNegativeMale))
print ("falseNegativeMale: " + str(falseNegativeMale))

accuracyBrand = ((truePositiveBrand + trueNegativeBrand) / 
                 (truePositiveBrand + trueNegativeBrand + falsePositiveBrand + falseNegativeBrand))
accuracyFemale = ((truePositiveFemale + trueNegativeFemale) / 
                  (truePositiveFemale + trueNegativeFemale + falsePositiveFemale + falseNegativeFemale))
accuracyMale = ((truePositiveMale + trueNegativeMale) / 
                 (truePositiveMale + trueNegativeMale + falsePositiveMale + falseNegativeMale))

print ("accuracyBrand: " + str(accuracyBrand))
print ("accuracyFemale: " + str(accuracyFemale))
print ("accuracyMale: " + str(accuracyMale))

precisionBrand = ((truePositiveBrand) / (truePositiveBrand + falsePositiveBrand))
precisionFemale = ((truePositiveFemale) / (truePositiveFemale + falsePositiveFemale))
precisionMale = ((truePositiveMale) / (truePositiveMale + falsePositiveMale))

print ("precisionBrand: " + str(precisionBrand))
print ("precisionFemale: " + str(precisionFemale))
print ("precisionMale: " + str(precisionMale))

recallBrand = ((truePositiveBrand) / (truePositiveBrand + falseNegativeBrand))
recallFemale = ((truePositiveFemale) / (truePositiveFemale + falseNegativeFemale))
recallMale = ((truePositiveMale) / (truePositiveMale + falseNegativeMale))

print ("recallBrand: " + str(recallBrand))
print ("recallFemale: " + str(recallFemale))
print ("recallMale: " + str(recallMale))

fmeasureBrand = ((2 * truePositiveBrand) / (2 * truePositiveBrand + falsePositiveBrand + falseNegativeBrand))
fmeasureFemale = ((2 * truePositiveFemale) / (2 * truePositiveFemale + falsePositiveFemale + falseNegativeFemale))
fmeasureMale = ((2 * truePositiveMale) / (2 * truePositiveMale + falsePositiveMale + falseNegativeMale))

print ("fmeasureBrand: " + str(fmeasureBrand))
print ("fmeasureFemale: " + str(fmeasureFemale))
print ("fmeasureMale: " + str(fmeasureMale))

specificityBrand = ((trueNegativeBrand) / (trueNegativeBrand + falsePositiveBrand))
specificityFemale = ((trueNegativeFemale) / (trueNegativeFemale + falsePositiveFemale))
specificityMale = ((trueNegativeMale) / (trueNegativeMale + falsePositiveMale))

print ("specificityBrand: " + str(specificityBrand))
print ("specificityFemale: " + str(specificityFemale))
print ("specificityMale: " + str(specificityMale))