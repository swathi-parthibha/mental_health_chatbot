from sent2vec.vectorizer import Vectorizer
from scipy import spatial
import json, random
from nltk.stem.snowball import SnowballStemmer

def execute(user_input): 
# get the user input 
	# user_input = input("Input: ")
	user_input = user_input
	# intents patterns are stored as in JSON 
	with open('intents.json', 'r') as f:
			data = json.load(f)

	# get the patterns from the intents and make them all lowercase
	patterns = [item["patterns"] for item in data["intents"]]
	patterns = [inner for outer in patterns for inner in outer]
	cleaned_patterns = [item.lower() for item in patterns]

	#dictionary that maps pattern to tag
	pattern_to_tag_dict = {}

	for item in data["intents"]: 
		for pattern in item["patterns"]: 
			pattern_to_tag_dict[pattern] = item["tag"]

	#dictionary that maps tag to a response
	tag_to_response = {}

	for item in data["intents"]: 
		tag_to_response[item["tag"]] = item["responses"]

	# remove unncessary punctuation 
	punctuation_to_remove = ["?", "!", ".", "\'", ","]
	cleaned_patterns = ["".join(
			[char for char in item if char not in punctuation_to_remove]) for item in cleaned_patterns]

	# add the input
	# clean the input by only keeping the words that are used as feature names
	user_input_words = [item.lower() for item in user_input.split(" ")]
	user_input_cleaned = ["".join(
			[char for char in item if char not in punctuation_to_remove]) for item in user_input_words]

	#implementing the snowball stemmer on the input
	stemmer = SnowballStemmer("english")
	user_input_stemmed = []
	for word in user_input_cleaned: 
		user_input_stemmed += [stemmer.stem(word)]

	#implementing the snowball stemmber of the patterns as well 
	for i in range(len(cleaned_patterns)): 
		pattern = ""
		word_lst = cleaned_patterns[i].split()
		for word in word_lst: 
			pattern = " ".join([pattern, stemmer.stem(word)])
		cleaned_patterns[i] = pattern

	# further cleans the input by removing words that are not in the pattern
	# we need to do this because the model created is using the words in the cleaned_patterns
	pattern_words = []
	for sentence in cleaned_patterns: 
		pattern_words += sentence.split()

	for word in user_input_stemmed: 
		if word not in pattern_words: 
			user_input_stemmed.remove(word)

	#creating a dictionary that maps each cleaned pattern to an index
	cleaned_pattern_to_index = {}
	count = 0
	for pattern in cleaned_patterns:
		cleaned_pattern_to_index[pattern] = count
		count += 1

	cleaned_patterns.append(" ".join(user_input_stemmed))

	# find the smallest dist and index where it was found
	min_dist = 1000
	min_index = 0

	vectorizer = Vectorizer(pretrained_weights='distilbert-base-multilingual-cased')
	vectorizer.run(cleaned_patterns)
	vectors = vectorizer.vectors

	for i in range(len(vectors) - 1):
		dist = spatial.distance.cosine(vectors[i], vectors[-1])

		if dist < min_dist: 
			min_dist = dist
			min_index = i
			
	pattern_found = cleaned_patterns[min_index]
	pattern_index = cleaned_pattern_to_index[pattern_found]
	original_pattern = patterns[pattern_index]
	tag = pattern_to_tag_dict[original_pattern]
	response = random.choice(tag_to_response[tag])

	return(tag)