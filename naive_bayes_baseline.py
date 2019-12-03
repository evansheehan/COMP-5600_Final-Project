import json
import Scrape

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
    prob_disliked = p_dislike
    prob_liked = p_like
    for word_comp in movie_comp:
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
print(results)