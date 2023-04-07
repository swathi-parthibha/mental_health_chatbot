import json
import numpy as np
from gensim.models import Word2Vec
from nltk.stem.snowball import SnowballStemmer


# get the user input 
user_input = input("Input: ")

# intents patterns are stored as in JSON 
with open('intents.json', 'r') as f:
    data = json.load(f)

# get the patterns from the intents and make them all lowercase
patterns = [item["patterns"] for item in data["intents"]]
patterns = [inner for outer in patterns for inner in outer]
cleaned_patterns = [item.lower() for item in patterns]

# remove unncessary punctuation 
punctuation_to_remove = ["?", "!", ".", "\'", ","]
cleaned_patterns = ["".join(
    [char for char in item if char not in punctuation_to_remove]) for item in cleaned_patterns]

# add the input
# cleans the input by removing punctuation
user_input_words = [item.lower() for item in user_input.split(" ")]
user_input_cleaned = ["".join(
    [char for char in item if char not in punctuation_to_remove]) for item in user_input_words]

#implementing the snowball stemmer on the input
stemmer = SnowballStemmer("english")
user_input_stemmed = []
for word in user_input_cleaned: 
	user_input_stemmed += [stemmer.stem(word)]

print(user_input_stemmed)

# further cleans the input by removing words that are not in the pattern
# we need to do this because the model created is using the words in the cleaned_patterns
pattern_words = []
for sentence in cleaned_patterns: 
	pattern_words += sentence.split()

for word in user_input_stemmed: 
	if word not in pattern_words: 
		user_input_stemmed.remove(word)

print(user_input_stemmed)

# trying the word2vec vectorizer
sentences = [sentence.split(" ") for sentence in cleaned_patterns]
model = Word2Vec(sentences=sentences, vector_size=100, window=5, min_count=1, workers=4)

# find the largest cosine similarity and index where it was found
max_cosine = 0
max_pattern = 0

for pattern in cleaned_patterns:
    # pattern words
	words = pattern.split(" ")
	v1 = np.array([model.wv[word] for word in words])

	# input words
	v2 = np.array([model.wv[word] for word in user_input_stemmed])

	l1 = np.mean(v1, axis=0)
	l2 = np.mean(v2, axis=0)

	cosine_sim = np.dot(l1/np.linalg.norm(l1), l2/np.linalg.norm(l2))

	# if the current similarity is higher than our previous max, set the current value to the max
	if cosine_sim > max_cosine: 
		max_cosine = cosine_sim
		max_pattern = pattern

print(max_cosine, max_pattern)

# ws1 = ['hi', "im", "sad"]
# ws2 = ['hi', "im", "sadness"]

# # these two are supposed to have the same output but not working !!!
# v1 = np.array([model.wv[word] for word in ws1])
# v2 = np.array([model.wv[word] for word in ws2])

# l1 = np.mean(v1, axis=0)
# l2 = np.mean(v2, axis=0)

# cosine = np.dot(l1/np.linalg.norm(l1), l2/np.linalg.norm(l2))
# print(cosine)