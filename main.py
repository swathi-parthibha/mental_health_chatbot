#This is the file where all the preprocessing of the data occurs

import json, random
import knn, naivebayes, bert
from collections import Counter



def execute_vote(user_input):

    with open('intents.json', 'r') as f:
       data = json.load(f)

    tag_to_response = {}

    for item in data["intents"]:
       tag_to_response[item["tag"]] = item["responses"]

    computed_tags = []

    knn_output = knn.execute_knn(user_input)
    bayes_output = naivebayes.execute_bayes(user_input, data)
    bert_output = bert.execute_bert(user_input, data)


    computed_tags.append(bert_output)
    computed_tags.append(knn_output)
    computed_tags.append(bayes_output)

    #Most common will be first, or if all 3 are different then bert output will be first because it was added to list first
    most_common_tag = Counter(computed_tags).most_common(3)[0][0]

    response = random.choice(tag_to_response[most_common_tag])
    print(response)
    return(response)

execute_vote("hi")