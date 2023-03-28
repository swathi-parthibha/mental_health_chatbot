import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
# word2vec - burt embeddings
# count vectorizer is most basic, tfidf slightly better, word2vec, contextial embeddings
# more complicated clustering algorithms, supervised clustering 


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

# create the vectorizer
vectorizer = TfidfVectorizer(
    max_df=0.8, min_df=1, max_features=1000, norm="l2")

# initial fit of the patterns
output_doc = vectorizer.fit_transform(cleaned_patterns).toarray()

# get the feature names 
index_to_vocab = {i: v for i, v in enumerate(vectorizer.get_feature_names_out())}

# clean the input by only keeping the words that are used as feature names
user_input_words = [item.lower() for item in user_input.split(" ")]
user_input_cleaned = ["".join(
    [char for char in item if char not in punctuation_to_remove]) for item in user_input_words]
user_input_exists = [word for word in user_input_cleaned if word in index_to_vocab.values()]

# add the user input to the existing patterns
cleaned_patterns.append(" ".join(user_input_exists))

# fit again with the user input 
output_doc = vectorizer.fit_transform(cleaned_patterns).toarray()
index_to_vocab = {i: v for i, v in enumerate(vectorizer.get_feature_names_out())}


# find the largest cosine similarity and index where it was found
max_cosine = 0
cosine_index = 0

for i in range(len(output_doc) - 1):
    # checking for divide by 0 condition
    if(np.linalg.norm(output_doc[i])) != 0:
        # cosine similarity formula
        cosine_sim = np.divide(np.dot(output_doc[-1], output_doc[i]), (np.linalg.norm(output_doc[i])))

        # if the current similarity is higher than our previous max, set the current value to the max
        if cosine_sim > max_cosine: 
            max_cosine = cosine_sim
            cosine_index = i

# print the pattern at the index found
print(cleaned_patterns[cosine_index])