# implement a naive bayes classifier
# multiclass classification (classes = tags)

import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

with open('intents.json', 'r') as f:
    data = json.load(f)


# this is the list of classes
tags = [item["tag"] for item in data["intents"]]

# this is the list of patterns
patterns = [item["patterns"] for item in data["intents"]]

# NOTE: removed "not really" from casual tag because the same pattern appeared twice
# we can change this, was just my quick fix
# this makes it so X.shape[0] == Y.shape[0] (n = 231)

# NOTE: removed this from intents
# {"tag": "no-response",
#         "patterns": [""],
#         "responses": ["Sorry, I didn't understand you.", "Please go on.", "Not sure I understand that.", "Please don't hesitate to talk to me."]
#  },

pattern_dict = {}
index = 0
for pattern_set in patterns:
    for pattern in pattern_set:
        pattern_dict.update({pattern.lower(): index})
    index += 1

patterns = [inner for outer in patterns for inner in outer]
patterns = [item.lower() for item in patterns]

# however, we don't want the training data to be in terms of strings
# we need a way to turn the strings into numbers!

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(patterns).toarray()
n = X.shape[0]  # num rows
Y = np.array([index for _, index in pattern_dict.items()])
classes = len(tags)

# should both have same number of rows
assert (X.shape[0] == Y.shape[0])


def naivebayesPY(x, y):
    """
    Input:
        x : n input vectors of d dimensions (nxd)
        y : n labels (nx1)

    Output:
    list probs : where probs[i] is the probability that y == i
    """
    n, d = np.shape(x)
    probs = np.zeros(classes)  # (should be the # of labels)
    for i in range(len(probs)):
        count = np.count_nonzero(y == i) / n
        probs[i] = count
    return probs


def PXY_mle_label(x, y, label):
    """
    Computation of P(X|Y) -- Maximum Likelihood Estimate
    Input:
        x : n input vectors of d dimensions (nxd)
        y : n labels (nx1)

    Output:
    prob: probability vector of p(x|y=label) (1xd)
    """

    n, d = np.shape(x)
    total_letters = 0
    count = []

    for i in range(0, d):
        num = 0
        for j in range(0, n):
            if y[j] == label:
                num += x[j][i]
                total_letters += x[j][i]
        count.append(num)
    print("total letters:", total_letters)

    prob = count / total_letters
    # print(prob)
    return prob


def naivebayesPXY_mle(x, y):
    """
    Computation of P(X|Y) -- Maximum Likelihood Estimate
    Input:
        x : n input vectors of d dimensions (nxd)
        y : n labels (nx1)

    Output:
    list probs: where probs[i] is the probability vector of p(x|y=i) (1xd)
    """
    n, d = np.shape(x)
    probs = np.zeros((classes, d))
    for i in range(classes):
        probs[i] = PXY_mle_label(x, y, i)
    return probs


def naivebayes(x, y, xtest):
    """
    Input:
    x : n input vectors of d dimensions (nxd)
    y : n labels

    Output:
    list probs: where probs[i] is the probability of P(y = i | x = xtest)
    """

    probsPXY = naivebayesPXY_mle(x, y)
    probsPY = naivebayesPY(x, y)
    probs = np.zeros(classes)
    m = 0
    prod_class = 1
    fact_denom = 1
    for num in range(classes):
        for a in range(len(xtest)):
            m += xtest[a]
            np.power(probsPXY[num][a], xtest[a])
            prod_class *= np.power(probsPXY[num][a], xtest[a])
            fact_denom *= np.math.factorial(xtest[a])

        coeff = (np.math.factorial(m))/fact_denom
        # i feel like just multiplying this here is wrong lol
        xtest_class = coeff * prod_class * probsPY[num]
        probs[num] = xtest_class
        m = 0
        prod_class = 1
        fact_denom = 1
    return probs


def classify(x, y, xtest):
    result = naivebayes(x, y, xtest)
    label = result.argmax()
    return label


xtest = vectorizer.transform(['I am feeling down']).toarray()[0]
print(pattern_dict)
print(classify(X, Y, xtest))

