import json
import math

#Based on TF-IDF
#Generate the inverted document frequency of a word given a list of documents
#Let's first generate how many documents this term occurs in.
def idf(term, documents):

    term_frequency = 0
    for movie in documents:
        if term in movie["Reviews"]:
            term_frequency += 1

    return math.log(len(documents)/term_frequency)

idf_dict = {}

in_file_name = "output/dataset/AllReviews_Reformatted_2_pruned.json"
out_file_name = "output/processing/IDF_Values.json"

with open(in_file_name, "r") as f:
    data = json.load(f)

for movie in data:
    for term in movie["Reviews"]:
        if term not in idf_dict:
            idf = idf(term, data)
            idf_dict.update({term: idf})
            print(term + " : " + str(idf))

with open(out_file_name, "w") as f:
    json.dump(idf_dict, f)
