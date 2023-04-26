# This is the file where all the preprocessing of the data occurs
#This is the file where all the preprocessing of the data occurs

import json
import random
import knn
import naivebayes
import bert
from collections import Counter
from nltk.stem.snowball import SnowballStemmer

with open('intents.json', 'r') as f:
    data = json.load(f)

patterns = []
tags = []
cleaned_patterns = []
pattern_dict = {}
cleaned_pattern_to_index = {}
pattern_to_tag_dict = {}
tag_to_response = {}


def init():
   for item in data["intents"]:
      tag_to_response[item["tag"]] = item["responses"]

   # get the patterns from the intents
   patterns = [item["patterns"] for item in data["intents"]]

   # this is the list of tags
   tags = [item["tag"] for item in data["intents"]]

   index = 0
   for pattern_set in patterns:
      for pattern in pattern_set:
         pattern_dict.update({pattern.lower(): index})
      index += 1

   patterns = [inner for outer in patterns for inner in outer]
   patterns = [item.lower() for item in patterns]

   # dictionary that maps pattern to tag
   for item in data["intents"]:
      for pattern in item["patterns"]:
         pattern_to_tag_dict[pattern] = item["tag"]

   # remove unncessary punctuation
   punctuation_to_remove = ["?", "!", ".", "\'", ","]
   cleaned_patterns = ["".join(
      [char for char in item if char not in punctuation_to_remove]) for item in patterns]

   # TODO: change to lemmatizer? Or get rid of this completely

   # stemmer = SnowballStemmer("english")
   # implementing the snowball stemmber of the patterns as well
   # for i in range(len(cleaned_patterns)):
   #    pattern = ""
   #    word_lst = cleaned_patterns[i].split()
   #    for word in word_lst:
   #       pattern = " ".join([pattern, stemmer.stem(word)])
   #    cleaned_patterns[i] = pattern

    # creating a dictionary that maps each cleaned pattern to an index
   count = 0
   for pattern in cleaned_patterns:
      cleaned_pattern_to_index[pattern] = count
      count += 1


def execute_vote(user_input):
    computed_tags = []
    knn_pattern = knn.execute_knn(user_input)
    bayes_pattern = naivebayes.execute_bayes(user_input, tags, patterns, pattern_dict)
    bert_pattern = bert.execute_bert(user_input, cleaned_patterns)



    for pattern in [knn_pattern, bayes_pattern, bert_pattern]:
      pattern_index = cleaned_pattern_to_index[pattern]
      original_pattern = patterns[pattern_index]
      tag = pattern_to_tag_dict[original_pattern]
      computed_tags.append(tag)

    # Most common will be first, or if all 3 are different then bert output will be first because it was added to list first
    most_common_tag = Counter(computed_tags).most_common(3)[0][0]

    response = random.choice(tag_to_response[most_common_tag])
    #  print(response)
    return (response)

# execute_vote("hi")
