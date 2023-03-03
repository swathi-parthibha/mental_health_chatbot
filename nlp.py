import json
from sklearn.feature_extraction.text import TfidfVectorizer

user_input = "Hi, I'm feeling down today"

with open('intents.json', 'r') as f:
    data = json.load(f)

patterns = [item["patterns"] for item in data["intents"]]
patterns = [inner for outer in patterns for inner in outer]
cleaned_patterns = [item.lower() for item in patterns]

punctuation_to_remove = ["?", "!", ".", "\'", ","]
cleaned_patterns = ["".join(
    [char for char in item if char not in punctuation_to_remove]) for item in cleaned_patterns]

vectorizer = TfidfVectorizer(
    max_df=0.7, min_df=1, max_features=1000, stop_words="english", norm="l2")
output_doc = vectorizer.fit_transform(cleaned_patterns).toarray()
