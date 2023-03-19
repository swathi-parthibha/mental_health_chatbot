import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

user_input = "Hi, I'm feeling down today random stuff"

with open('intents.json', 'r') as f:
    data = json.load(f)

patterns = [item["patterns"] for item in data["intents"]]
patterns = [inner for outer in patterns for inner in outer]
cleaned_patterns = [item.lower() for item in patterns]

punctuation_to_remove = ["?", "!", ".", "\'", ","]
cleaned_patterns = ["".join(
    [char for char in item if char not in punctuation_to_remove]) for item in cleaned_patterns]

vectorizer = TfidfVectorizer(
    max_df=0.8, min_df=1, max_features=1000, norm="l2")

output_doc = vectorizer.fit_transform(cleaned_patterns).toarray()

index_to_vocab = {i: v for i, v in enumerate(vectorizer.get_feature_names())}

user_input_words = [item.lower() for item in user_input.split(" ")]
user_input_cleaned = ["".join(
    [char for char in item if char not in punctuation_to_remove]) for item in user_input_words]
user_input_exists = [word for word in user_input_cleaned if word in index_to_vocab.values()]
print(user_input_exists)

