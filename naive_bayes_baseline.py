import json
import numpy as np

# import the list of movies
from typing import List, Any

movies = []
with open("AllReviews_Reformatted_2.json") as f:
    data = json.load(f)
    for movie in data:
        movie["Title"] = str.strip(movie["Title"][0])
        movies.append(movie)

# get 3 movies the user liked and disliked
l_1 = "Frozen" #input("Enter a movie you enjoyed: ")
l_2 = "Toy Story" #input("Enter another movie you enjoyed: ")
l_3 = "Moana" #input("Enter a third movie you enjoyed: ")

d_1 = "The Lighthouse" #input("Enter a movie you hated: ")
d_2 = "Parasite" #input("Enter another movie you hated: ")
d_3 = "Whiplash" #input("Enter a third movie you hated: ")

input_list = [l_1, l_2, l_3, d_1, d_2, d_3]

# get all 6 movie objects (may need to correct for case and have a fail case)
liked_movies = []
disliked_movies = []

for movie in movies:
    movie_title = str.strip(movie["Title"])
    if movie_title in input_list:
        if input_list.index(movie_title) < 3:
            liked_movies.append(movie)
        else:
            disliked_movies.append(movie)

assert len(liked_movies) == 3
assert len(disliked_movies) == 3

"""liked_1 = next(movie for movie in movies if movie["Title"][0] == l_1)
liked_2 = next(movie for movie in movies if movie["Title"][0] == l_2)
liked_3 = next(movie for movie in movies if movie["Title"][0] == l_3)
disliked_1 = next(movie for movie in movies if movie["Title"][0] == d_1)
disliked_2 = next(movie for movie in movies if movie["Title"][0] == d_2)
disliked_3 = next(movie for movie in movies if movie["Title"][0] == d_3)"""

# populate two new dictionaries of liked and disliked reviews
liked_dict = {}
disliked_dict = {}
#distinct_words = {}

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
p_like = like_sum/(vocabulary_sum)
p_dislike = dislike_sum/(vocabulary_sum)

"""prob_word_given_like = {}
prob_word_given_dislike = {}"""

"""for word in liked_dict:
    prob = (liked_dict[word] + 1)/(like_sum + vocabulary_sum)
    prob_word_given_like.update({word: prob})

for word in disliked_dict:
    prob = (disliked_dict[word] + 1)/(dislike_sum + vocabulary_sum)
    prob_word_given_dislike.update({word: prob})"""

best_movie = ["", -1]
worst_movie = ["", -1]

results = []

for movie in movies:
    if movie["Reviews"] != None and movie["Title"] not in input_list:
        like_probabilities = []
        dislike_probabilities = []
        for word in movie["Reviews"]:

            try:
                prob_word_given_like = ((liked_dict.get(word) + 1)/(like_sum + len(liked_dict)))**movie["Reviews"].get(word)
            except:
                prob_word_given_like = 1 / (like_sum + len(liked_dict))
            try:
                prob_word_given_dislike = ((disliked_dict.get(word) + 1)/(dislike_sum + len(disliked_dict)))**movie["Reviews"].get(word)
            except:
                prob_word_given_dislike = 1 / (dislike_sum + len(disliked_dict))

            like_probabilities.append(prob_word_given_like)
            dislike_probabilities.append(prob_word_given_dislike)

        
        probability_like_movie = p_like*(np.product(like_probabilities))
        probability_dislike_movie = p_dislike*(np.product(dislike_probabilities))

        #Add to results array
        movie_to_add = []
        movie_to_add.append(movie["Title"])
        movie_to_add.append(probability_like_movie)
        movie_to_add.append(probability_dislike_movie)
        movie_to_add.append(abs(probability_like_movie-probability_dislike_movie))
        results.append(movie_to_add)

        if probability_like_movie > best_movie[1]:
            best_movie[0] = movie["Title"]
            best_movie[1] = probability_like_movie

        if probability_dislike_movie > worst_movie[1]:
            worst_movie[0] = movie["Title"]
            worst_movie[1] = probability_dislike_movie

    #print("Probability you will like " + movie["Title"] + " is: " + str(probability_like_movie))
    #print("Probability you will dislike " + movie["Title"] + " is: " + str(probability_dislike_movie))

print(best_movie)
print(worst_movie)


"""print("Probability " + word + " shows up in a liked movie: "
+ str(prob_word_given_like.get(word)) + "\nProbability " + word
+ " shows up in a disliked movie: " + str(prob_word_given_dislike.get(word)) + "\n")"""

# iterate over the movie list, using naive bayes to calculate probabilities
# we need to make an dict of doubles and movie titles to store our results
"""for movie_comp in movies:
    # needed to make the next for loop work?
    
    #assert isinstance(movie_comp, movie)

    # for our results array
    result_str = movie_comp["Title"]
    prob_disliked = p_dislike
    prob_liked = p_like
    dict_comp = movie_comp["Reviews"]
    numerator = 0
    denominator = like_sum
    
    for word_comp in dict_comp:

        for dictionary in liked_dict:
            for word in dictionary:
                #if word_compare 
                if word_comp[1] == word[1]:
                    numerator += min(word_comp[0], word[0])
                    break
    
    prob_liked = prob_liked * (numerator/denominator) * 


        # no clue if this is how you do it but I want to find the word in liked_dict that is equal to word_comp
        word_1 = next(object for word in liked_dict if word_comp == liked_dict[1])
        # we take this word and set its count as the numerator
        numerator = word_1[0]
        # number of distinct words in liked_dict is denominator
        denominator = liked_dict.sizeof()
        # divide then multiply by the number of times this word appears
        prob_liked = prob_liked * (numerator/denominator) * word_comp[0]
        # now we repeat for disliked
        # no clue if this is how you do it but I want to find the word in liked_dict that is equal to word_comp
        word_2 = next(object for word in disliked_dict if word_comp == disliked_dict[1])
        # we take this word and set its count as the numerator
        numerator = word_1[0]
        # number of distinct words in liked_dict is denominator
        denominator = disliked_dict.sizeof()
        # divide then multiply by the number of times this word appears
        prob_disliked = prob_disliked * (numerator / denominator) * word_comp[0]
    # append this movie and it's probabilities to our results
    results.append({"Title": result_str, "Like": prob_liked, "Dislike": prob_disliked})
print(results)"""