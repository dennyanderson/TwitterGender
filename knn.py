import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from collections import Counter

from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix

class MultiColumnLabelEncoder:
    def __init__(self,columns = None):
        self.columns = columns # array of column names to encode

    def fit(self,X,y=None):
        return self # not relevant here

    def transform(self,X):
        '''
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        '''
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

# define column names
names = ['fav_number', 'link_color', 'retweet_count', 'sidebar_color', 'tweet_count', 'gender']

# loading training data
df = pd.read_csv('genderCSVedit.csv', header=None, names=names)
df.head()

gender_df = pd.DataFrame(df)

transformed = MultiColumnLabelEncoder(columns = ['link_color', 'sidebar_color', 'gender']).fit_transform(gender_df)

# making our predictions 
predictions = []

# create design matrix X and target vector y
X = np.array(transformed.ix[:, :5])     # end index is exclusive
y = np.array(transformed['gender'])   # another way of indexing a pandas df

# split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# creating odd list of K for KNN
myList = list(range(1,50))

# subsetting just the odd ones
neighbors = list(filter(lambda x: x % 2 != 0, myList))

# empty list that will hold cross validation scores
cv_scores = []

# perform 10-fold cross validation we are already familiar with
for k in neighbors:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X_train, y_train, cv=10, scoring='accuracy')
    cv_scores.append(scores.mean())

# changing to misclassification error
MSE = [1 - x for x in cv_scores]

# Let's try to discover what is the best value of k
# Run the following cell to show the table
# determining best k
optimal_k = neighbors[MSE.index(min(MSE))]
print("The optimal number of neighbors is %d" % optimal_k)

def train(X_train, y_train):
    # do nothing 
    return

from collections import Counter

def predict(X_train, y_train, x_test, k):
    # create list for distances and targets
    distances = []
    targets = []

    for i in range(len(X_train)):
        # first we compute the Euclidean distance
        # (use x_test and X_train[i, :]. Also, where appropriate, you can use np.sqrt, np.square, and np.sum...)
        distance = np.sqrt(np.sum(np.square(x_test - X_train[i, :])))
        # add it to list of distances
        distances.append([distance, i])

    # sort the list
    distances = sorted(distances)

    # make a list of the k neighbors' targets
    for i in range(k):
        # (Hint: index receives particular value in distances[something][something])
        index = distances[i][1]
        # (Hint: use y_train and index below)
        targets.append(y_train[index])

    # return most common target
    return Counter(targets).most_common(1)[0][0]

from sklearn.metrics import accuracy_score

def kNearestNeighbor(X_train, y_train, X_test, predictions, k):
    # train on the input data
    train(X_train, y_train)

    # loop over all observations
    for i in range(len(X_test)):
        predictions.append(predict(X_train, y_train, X_test[i, :], k))
        
# making our predictions 
# Using the optimal value of K discovered above
predictions = []
try:
    optimalK = 33 # Add your answer here (and delete line!)
    kNearestNeighbor(X_train, y_train, X_test, predictions, optimalK)
    predictions = np.asarray(predictions)

    # evaluating accuracy
    accuracy = accuracy_score(y_test, predictions) * 100
    print('\nThe accuracy of OUR classifier is %d%%' % accuracy)
    print(confusion_matrix(y_test, predictions))

except ValueError:
    print('Can\'t have more neighbors than training samples!!') # Need to be careful about value of k