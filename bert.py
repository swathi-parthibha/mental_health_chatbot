from sent2vec.vectorizer import Vectorizer
from scipy import spatial
import json
import random
from nltk.stem.snowball import SnowballStemmer


def execute_bert(user_input, cleaned_patterns):
    punctuation_to_remove = ["?", "!", ".", "\'", ","]

    # clean the input by only keeping the words that are used as feature names
    user_input_words = [item.lower() for item in user_input.split(" ")]
    user_input_cleaned = ["".join(
        [char for char in item if char not in punctuation_to_remove]) for item in user_input_words]

    # implementing the snowball stemmer on the input
    stemmer = SnowballStemmer("english")
    user_input_stemmed = []
    for word in user_input_cleaned:
        user_input_stemmed += [stemmer.stem(word)]

    # # further cleans the input by removing words that are not in the pattern
    # # we need to do this because the model created is using the words in the cleaned_patterns
    # pattern_words = []
    # for sentence in cleaned_patterns:
    #     pattern_words += sentence.split()

    # for word in user_input_stemmed:
    #     if word not in pattern_words:
    #         user_input_stemmed.remove(word)

    cleaned_patterns.append(" ".join(user_input_stemmed))

    # find the smallest dist and index where it was found
    min_dist = 1000
    min_index = 0

    vectorizer = Vectorizer(
        pretrained_weights='distilbert-base-multilingual-cased')
    vectorizer.run(cleaned_patterns)
    vectors = vectorizer.vectors

    for i in range(len(vectors) - 1):
        dist = spatial.distance.cosine(vectors[i], vectors[-1])

        if dist < min_dist:
            min_dist = dist
            min_index = i

    pattern_found = cleaned_patterns[min_index]

    return pattern_found
