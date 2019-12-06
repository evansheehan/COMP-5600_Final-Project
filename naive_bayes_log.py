import json
import math
import numpy as np
import error_analysis

# import the list of movies
from typing import List, Any

def run_nb_log():

    movies = []
    with open("AllReviews_Reformatted_2_pruned.json") as f:
        data = json.load(f)
        for movie in data:
            movie["Title"] = str.strip(movie["Title"][0])
            movies.append(movie)

    # # get 3 movies the user liked and disliked
    # l_1 = "Whiplash" #input("Enter a movie you enjoyed: ")
    # l_2 = "First Man" #input("Enter another movie you enjoyed: ")
    # l_3 = "I Saw the Devil" #input("Enter a third movie you enjoyed: ")

    # d_1 = "Frozen" #input("Enter a movie you hated: ")
    # d_2 = "Parasite" #input("Enter another movie you hated: ")
    # d_3 = "Moana" #input("Enter a third movie you hated: ")

    liked_list = []

    with open("liked_training_set.json") as f:
        data = json.load(f)
        liked_list = data
    
    disliked_list = []

    with open("disliked_training_set.json") as f:
        data = json.load(f)
        disliked_list = data

    # get all 6 movie objects (may need to correct for case and have a fail case)
    liked_movies = []
    disliked_movies = []
    liked_and_disliked_movies = []

    for movie in movies:
        movie_title = str.strip(movie["Title"])
        if movie_title in liked_list:
            if movie["Reviews"] != None:
                liked_movies.append(movie)
                liked_and_disliked_movies.append(movie)
        elif movie_title in disliked_list:    
            if movie["Reviews"] != None:
                disliked_movies.append(movie)
                liked_and_disliked_movies.append(movie)

    assert len(liked_movies) > 0
    assert len(disliked_movies) > 0

    # populate two new dictionaries of liked and disliked reviews
    liked_dict = {}
    disliked_dict = {}
    cumulative_dict = {}

    for movie in liked_movies:
        assert movie["Reviews"] != None, movie["Title"] + " has no reviews."
        reviews = list(movie["Reviews"].items())
        for review in reviews:
            word = review[0]
            count = review[1]
            if word in liked_dict:
                liked_dict[word] = liked_dict.get(word) + count
            else:
                liked_dict.update({word: count})

    for movie in disliked_movies:
        assert movie["Reviews"] != None, movie["Title"] + " has no reviews."
        reviews = list(movie["Reviews"].items())
        for review in reviews:
            word = review[0]
            count = review[1]
            if word in disliked_dict:
                disliked_dict[word] = disliked_dict.get(word) + count
            else:
                disliked_dict.update({word: count})

    for movie in liked_and_disliked_movies:
        assert movie["Reviews"] != None, movie["Title"] + " has no reviews."
        reviews = list(movie["Reviews"].items())
        for review in reviews:
            word = review[0]
            count = review[1]
            if word in cumulative_dict:
                cumulative_dict[word] = cumulative_dict.get(word) + count
            else:
                cumulative_dict.update({word: count})

    # instantiate comparison variables
    p_like = 0.0
    p_dislike = 0.0

    # add up all the words total in the liked dict and disliked_dict
    vocabulary_sum = 0

    like_sum = 0
    for word in liked_dict:
        like_sum += liked_dict[word] 
        #like_sum = word[0] + like_sum

    dislike_sum = 0
    for word in disliked_dict:
        dislike_sum += disliked_dict[word]
        #dislike_sum = word[0] + dislike_sum

    vocabulary_sum = like_sum + dislike_sum

    # calculate word count difference between liked and disliked and present the two as a ratio
    # p_like = 0.5
    # p_dislike = 0.5
    p_like = math.log1p(like_sum/(vocabulary_sum))
    p_dislike = math.log1p(dislike_sum/(vocabulary_sum))

    best_movie = ["", -1]
    worst_movie = ["", 1]

    results = []

    liked_test_set = []
    disliked_test_set = []
    cumulative_test_set = []

    with open("liked_test_set.json", "r") as f:
        liked_test_set = json.load(f)

    with open("disliked_test_set.json", "r") as f:
        disliked_test_set = json.load(f)

    for movie in liked_test_set:
        cumulative_test_set.append(movie)
    for movie in disliked_test_set:
        cumulative_test_set.append(movie)
    

    for movie in movies:
        if movie["Reviews"] != None and movie["Title"] in cumulative_test_set:
            like_probabilities = []
            dislike_probabilities = []
            for word in movie["Reviews"]:

                try:
                    prob_word_given_like = math.log1p(((liked_dict.get(word) + 1)/(like_sum + len(cumulative_dict))))#*movie["Reviews"].get(word))
                except:
                    prob_word_given_like = math.log1p(1 / (like_sum + len(cumulative_dict)))
                try:
                    prob_word_given_dislike = math.log1p(((disliked_dict.get(word) + 1)/(dislike_sum + len(cumulative_dict))))#*movie["Reviews"].get(word)
                except:
                    prob_word_given_dislike = math.log1p(1 / (dislike_sum + len(cumulative_dict)))

                like_probabilities.append(prob_word_given_like)
                dislike_probabilities.append(prob_word_given_dislike)

            
            probability_like_movie = math.log1p(p_like)+(np.sum(like_probabilities))
            probability_dislike_movie = math.log1p(p_dislike)+(np.sum(dislike_probabilities))

            #Add to results array
            movie_to_add = []
            movie_to_add.append(movie["Title"])
            movie_to_add.append(probability_like_movie)
            movie_to_add.append(probability_dislike_movie)
            delta_prob = probability_like_movie-probability_dislike_movie
            sum_prob = probability_like_movie+probability_dislike_movie
            movie_to_add.append(delta_prob)
            results.append(movie_to_add)

            if (delta_prob) > best_movie[1]:
                best_movie[0] = movie["Title"]
                best_movie[1] = delta_prob

            if (delta_prob) < worst_movie[1]:
                worst_movie[0] = movie["Title"]
                worst_movie[1] = delta_prob

    print(best_movie)
    print(worst_movie)

    results, accuracy = error_analysis.generate_error_rate(liked_test_set, disliked_test_set, results)

    #This should find our questionable results
    if accuracy < 0.3:
        print("\nSurprise! You got questionable results...here's the results array and their deltas:")
        for movie in results: print([movie[0], movie[3]])

        print("\nHere's the liked test set in this case:")
        for movie in liked_test_set: print(movie)

        print("\nHere's the disliked test set in this case:")
        for movie in disliked_test_set: print(movie)

    def sort_value(val):
        return val[3]
    results.sort(key = sort_value, reverse = True)
    with open("results_output.json", "w") as f:
        json.dump(results, f)

    return results, accuracy