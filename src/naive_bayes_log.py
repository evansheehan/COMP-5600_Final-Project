import json
import math
import numpy as np
import error_analysis
import misc_algorithms
import binormal_separation as bns

# import the list of movies
from typing import List, Any

#Takes a single boolean as a parameter determining whether you want to run test/training data or manually input data
def run_nb_log(testing):

    movies = []
    directory = "output/dataset/"
    with open(directory + "AllReviews_Reformatted_2_pruned.json", "r") as f:
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
    disliked_list = []

    #If runnings tests, use the generated training sets
    if testing:
        directory = "output/generated_sets/"
        with open(directory + "liked_training_set.json", "r") as f:
            data = json.load(f)
            liked_list = data
        with open(directory + "disliked_training_set.json", "r") as f:
            data = json.load(f)
            disliked_list = data
    
    #If not testing, manually append. This will be user input in the future.
    else:
        liked_list.append("Toy Story")
        liked_list.append("Toy Story 2")
        disliked_list.append("Get Out")
        disliked_list.append("As Above So Below")

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

    #Run BNS algorithm on all terms
    # bns_dict = bns.run_bns(liked_and_disliked_movies, liked_movies, disliked_movies)

    # populate two new dictionaries of liked and disliked reviews
    liked_dict, disliked_dict, cumulative_dict = misc_algorithms.generate_dicts(liked_movies, disliked_movies, liked_and_disliked_movies)

    # instantiate comparison variables
    p_like = 0.0
    p_dislike = 0.0

    #Calculate total word count in dictionaries
    like_sum = 0
    dislike_sum = 0
    vocabulary_sum = 0

    for word in liked_dict:
        like_sum += liked_dict[word] 
    for word in disliked_dict:
        dislike_sum += disliked_dict[word]
    vocabulary_sum = like_sum + dislike_sum

    # calculate word count difference between liked and disliked and present the two as a ratio
    # p_like = 0.5
    # p_dislike = 0.5
    p_like = math.log1p(like_sum/(vocabulary_sum))
    p_dislike = math.log1p(dislike_sum/(vocabulary_sum))

    best_movie = ["", -1]
    worst_movie = ["", 1]
    results = []

    if testing:
    #Use the generated test sets if testing
        liked_test_set = []
        disliked_test_set = []
        cumulative_test_set = []

        directory = "output/generated_sets/"
        with open(directory + "liked_test_set.json", "r") as f:
            liked_test_set = json.load(f)

        with open(directory + "disliked_test_set.json", "r") as f:
            disliked_test_set = json.load(f)

        for movie in liked_test_set:
            cumulative_test_set.append(movie)
        for movie in disliked_test_set:
            cumulative_test_set.append(movie)
    
    #Not testing...the test set should be the entire dataset
    else:
        cumulative_test_set = []
        for movie in movies:
            cumulative_test_set.append(movie["Title"])
    

    for movie in movies:
        if movie["Reviews"] != None and movie["Title"] in cumulative_test_set:
            like_probabilities = []
            dislike_probabilities = []
            for word in movie["Reviews"]:

                try:
                    prob_word_given_like = math.log1p(((liked_dict.get(word) + 1)/(like_sum))) #+ len(cumulative_dict))))#*movie["Reviews"].get(word))
                except:
                    prob_word_given_like = math.log1p(1 / (like_sum)) #+ len(cumulative_dict)))
                try:
                    prob_word_given_dislike = math.log1p(((disliked_dict.get(word) + 1)/(dislike_sum))) #+ len(cumulative_dict))))#*movie["Reviews"].get(word)
                except:
                    prob_word_given_dislike = math.log1p(1 / (dislike_sum)) #+ len(cumulative_dict)))

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

    if testing:
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
    directory = "output/results/"
    with open(directory + "results_output.json", "w") as f:
        json.dump(results, f)

    if testing:
        return results, accuracy
    else:
        return results