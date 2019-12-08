from scipy.stats import norm
import math

#Implementation of https://www.hpl.hp.com/techreports/2007/HPL-2007-32R1.pdf

def bns(term, liked_movies, disliked_movies):

    #True and false positive rates (tp/pos and fp/neg)
    tpr = 0
    fpr = 0

    #Number of times word occurs in positive and negative training cases
    tp = 0
    fp = 0

    #Number of positive and negative documents
    pos = len(liked_movies)
    neg = len(disliked_movies)

    for movie in liked_movies:
        if term in movie["Reviews"]:
            tp += 1

    for movie in disliked_movies:
        if term in movie["Reviews"]:
            fp += 1

    tpr = tp/pos
    fpr = fp/neg

    bns_result = abs(norm.ppf(tpr) - norm.ppf(fpr))

    #Max and min for algorithm
    if bns_result < 0.0005 or math.isinf(bns_result) or math.isnan(bns_result): bns_result = 0.0005
    elif bns_result > 1: bns_result = 1

    return bns_result

def run_bns(documents, liked_movies, disliked_movies):

    bns_dict = {}

    progress = 0
    documents_size = len(documents)

    for movie in documents:
        for term in movie["Reviews"]:
            if term not in bns_dict:
                bns_result = bns(term, liked_movies, disliked_movies)
                bns_dict.update({term: bns_result})
        progress += 1
        print(str(progress) + "/" + str(documents_size))

    return bns_dict
