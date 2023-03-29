from sent2vec.vectorizer import Vectorizer
from scipy import spatial
import json

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
# clean the input by only keeping the words that are used as feature names
user_input_words = [item.lower() for item in user_input.split(" ")]
user_input_cleaned = ["".join(
    [char for char in item if char not in punctuation_to_remove]) for item in user_input_words]

cleaned_patterns.append(" ".join(user_input_cleaned))

# find the smallest dist and index where it was found
min_dist = 0
min_index = 0

vectorizer = Vectorizer(pretrained_weights='distilbert-base-multilingual-cased')
vectorizer.run(cleaned_patterns)
vectors = vectorizer.vectors

for i in range(len(vectors) - 1):
	dist = spatial.distance.cosine(vectors[i], vectors[-1])
	print(dist)

	if dist < min_dist: 
		min_dist = dist
		min_index = i
    
# print the pattern at the index found
print(cleaned_patterns[min_index])