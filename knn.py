# implement a k nearest neighbors classifier
# k -> fit this number to find best accuracy

# exact same set up as naivebayes.py

import json
import numpy as np
import math
from sklearn.feature_extraction.text import CountVectorizer

with open('intents.json', 'r') as f:
    data = json.load(f)


# this is the list of classes
tags = [item["tag"] for item in data["intents"]]

# this is the list of patterns
patterns = [item["patterns"] for item in data["intents"]]

pattern_dict = {}
index = 0
for pattern_set in patterns:
    for pattern in pattern_set:
        pattern_dict.update({pattern.lower(): index})
    index += 1

patterns = [inner for outer in patterns for inner in outer]
patterns = [item.lower() for item in patterns]

vectorizer = CountVectorizer(
    max_df=0.7, min_df=1)
X = vectorizer.fit_transform(patterns).toarray()
n = X.shape[0]  # num rows
Y = np.array([[index] for _, index in pattern_dict.items()])

X_train = np.hstack((X, Y))

# should both have same number of rows
assert (X.shape[0] == Y.shape[0])


def distance(x, xtest):
  """
  Input:
  x: input vector of length d
  xtest: input test vector of length d

  Output:
  distance = euclidean distance between x and xtest
  """
  distance = 0.0
  for i in range(len(x)-1): # last entry is the label
    distance += (x[i] - xtest[i])**2
  return math.sqrt(distance)


def nearest_neighbors(X_train, xtest, k=5):
  distances = list()

  for xi in X_train:
    dist = distance(xi, xtest)
    distances.append((xi, dist))

  distances.sort(key=lambda pair: pair[1]) # sorts by distance

  neighbors = [elt[0] for elt in distances[:k]] # gets the first k elements in the list

  # the problem is that with ties, it breaks them by picking the smallest number label,
  # which isn't right if we have a direct match
  # get around this setting all neighbors equal if dist == 0
  if (distances[0][1] == 0):
    neighbors = list()
    for i in range(k):
       neighbors.append(distances[0][0])
  return neighbors

def knn_classify(X_train, xtest, k=5):
  neighbors = nearest_neighbors(X_train, xtest, k)
  neighbor_labels = [neighbor[-1] for neighbor in neighbors] # label concatenated to training data
  prediction = max(set(neighbor_labels), key=neighbor_labels.count)
  return prediction


xtest = vectorizer.transform(['Good afternoon']).toarray()[0]
print(knn_classify(X_train, xtest, k=5))