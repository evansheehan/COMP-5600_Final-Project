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

    for movie in movies:
        movie_title = str.strip(movie["Title"])
        if movie_title in liked_list:
            if movie["Reviews"] != None:
                liked_movies.append(movie)
        if movie_title in disliked_list:    
            if movie["Reviews"] != None:
                disliked_movies.append(movie)

    assert len(liked_movies) > 0
    assert len(disliked_movies) > 0

    """liked_1 = next(movie for movie in movies if movie["Title"][0] == l_1)
    liked_2 = next(movie for movie in movies if movie["Title"][0] == l_2)
    liked_3 = next(movie for movie in movies if movie["Title"][0] == l_3)
    disliked_1 = next(movie for movie in movies if movie["Title"][0] == d_1)
    disliked_2 = next(movie for movie in movies if movie["Title"][0] == d_2)
    disliked_3 = next(movie for movie in movies if movie["Title"][0] == d_3)"""

    # populate two new dictionaries of liked and disliked reviews
    liked_dict = {}
    disliked_dict = {}

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
    p_like = 0.5
    p_dislike = 0.5
    """p_like = math.log1p(like_sum/(vocabulary_sum))
    p_dislike = math.log1p(dislike_sum/(vocabulary_sum))"""

    """prob_word_given_like = {}
    prob_word_given_dislike = {}"""

    """for word in liked_dict:
        prob = (liked_dict[word] + 1)/(like_sum + vocabulary_sum)
        prob_word_given_like.update({word: prob})

    for word in disliked_dict:
        prob = (disliked_dict[word] + 1)/(dislike_sum + vocabulary_sum)
        prob_word_given_dislike.update({word: prob})"""

    best_movie = ["", -1]
    worst_movie = ["", 1]

    results = []

    liked_test_set = []
    disliked_test_set = []
    test_set = []

    with open("liked_test_set.json", "r") as f:
        liked_test_set = json.load(f)

    with open("disliked_test_set.json", "r") as f:
        disliked_test_set = json.load(f)

    for movie in movies:
        if movie["Reviews"] != None and movie["Title"] in (liked_test_set or disliked_test_set):
            like_probabilities = []
            dislike_probabilities = []
            for word in movie["Reviews"]:

                try:
                    prob_word_given_like = math.log1p(((liked_dict.get(word) + 1)/(like_sum + len(liked_dict))))*movie["Reviews"].get(word)
                except:
                    prob_word_given_like = math.log1p(1 / (like_sum + len(liked_dict)))
                try:
                    prob_word_given_dislike = math.log1p(((disliked_dict.get(word) + 1)/(dislike_sum + len(disliked_dict))))*movie["Reviews"].get(word)
                except:
                    prob_word_given_dislike = math.log1p(1 / (dislike_sum + len(disliked_dict)))

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
            movie_to_add.append(-delta_prob)
            results.append(movie_to_add)

            if (delta_prob) > best_movie[1]:
                best_movie[0] = movie["Title"]
                best_movie[1] = delta_prob

            if (delta_prob) < worst_movie[1]:
                worst_movie[0] = movie["Title"]
                worst_movie[1] = delta_prob

        #print("Probability you will like " + movie["Title"] + " is: " + str(probability_like_movie))
        #print("Probability you will dislike " + movie["Title"] + " is: " + str(probability_dislike_movie))

    print(best_movie)
    print(worst_movie)

    accuracy = error_analysis.generate_error_rate(liked_test_set, disliked_test_set, results)

    def sort_value(val):
        return val[3]
    results.sort(key = sort_value, reverse = True)
    with open("results_output.json", "w") as f:
        json.dump(results, f)

    return accuracy
    """import json
    import math

    # import the list of movies
    from typing import List, Any

    movies = []
    with open("Iteration0.json") as f:
        data = json.load(f)
        for movie in data:
            movies.append(movie)

    # get 3 movies the user liked and disliked
    l_1 = input("Enter a movie you enjoyed: ")
    l_2 = input("Enter another movie you enjoyed: ")
    l_3 = input("Enter a third movie you enjoyed: ")

    d_1 = input("Enter a movie you hated: ")
    d_2 = input("Enter another movie you hated: ")
    d_3 = input("Enter a third movie you hated: ")

    # get all 6 movie objects (may need to correct for case and have a fail case)
    liked_1 = next(movie for movie in movies if movie["Title"] == l_1)
    liked_2 = next(movie for movie in movies if movie["Title"] == l_2)
    liked_3 = next(movie for movie in movies if movie["Title"] == l_3)
    disliked_1 = next(movie for movie in movies if movie["Title"] == d_1)
    disliked_2 = next(movie for movie in movies if movie["Title"] == d_2)
    disliked_3 = next(movie for movie in movies if movie["Title"] == d_3)

    # populate two new dictionaries of liked and disliked reviews
    liked_dict: List[Any] = []
    disliked_dict = []
    liked_dict.append(liked_1, liked_2, liked_3)
    disliked_dict.append(disliked_1, disliked_2, disliked_3)

    # instantiate comparison variables
    p_like = 0.0
    p_dislike = 0.0

    # add up all the words total in the liked dict and disliked_dict
    like_sum = 0
    for word in liked_dict:
        like_sum = word[0] + like_sum
    dislike_sum = 0
    for word in disliked_dict:
        dislike_sum = word[0] + dislike_sum

    # calculate word count difference between liked and disliked and present the two as a ratio
    p_like = like_sum/(like_sum + dislike_sum)
    p_dislike = dislike_sum/(like_sum + dislike_sum)

    # iterate over the movie list, using naive bayes to calculate probabilities
    # we need to make an dict of doubles and movie titles to store our results
    results = []
    for movie_comp in movies:
        # needed to make the next for loop work?
        assert isinstance(movie_comp, movie)
        # for our results array
        result_str = movie_comp['Title']
        prob_disliked = math.log(p_dislike)
        prob_liked = math.log(p_like)
        for word_comp in movie_comp:
            # no clue if this is how you do it but I want to find the word in liked_dict that is equal to word_comp
            word_1 = next(object for word in liked_dict if word_comp == liked_dict[1])
            # we take this word and set its count as the numerator
            numerator = word_1[0]
            # number of distinct words in liked_dict is denominator
            denominator = liked_dict.sizeof()
            # divide then multiply by the number of times this word appears
            prob_liked = math.log(prob_liked) + (math.log((numerator/denominator)) * word_comp[0])
            # now we repeat for disliked
            # no clue if this is how you do it but I want to find the word in liked_dict that is equal to word_comp
            word_2 = next(object for word in disliked_dict if word_comp == disliked_dict[1])
            # we take this word and set its count as the numerator
            numerator = word_1[0]
            # number of distinct words in liked_dict is denominator
            denominator = disliked_dict.sizeof()
            # divide then multiply by the number of times this word appears
            prob_disliked = math.log(prob_disliked) + (math.log((numerator / denominator)) * word_comp[0])
        # append this movie and it's probabilities to our results
        results.append({"Title": result_str, "Like": prob_liked, "Dislike": prob_disliked})
    print(results)"""
