# implement a k means clustering classifier
# k = # of tags

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

def distance(x, xtest):
    """
    Input:
    x: input vector of length d
    xtest: input test vector of length d

    Output:
    distance = euclidean distance between x and xtest
    """
    distance = 0.0
    for i in range(len(x)-1):  # last entry is the label
        distance += (x[i] - xtest[i])**2
    return math.sqrt(distance)



X_train = np.hstack((X, Y)) # this is each training vector concatenated with the label

# should both have same number of rows
assert (X.shape[0] == Y.shape[0])

def distances(x, xtest):
  """
  Input:
  X: n input vectors of length d
  xtest: input test vector of length d

  Output:
  distance = euclidean distance between x and xtest
  """
  return np.sqrt(np.sum((X - xtest)**2, axis=1))

