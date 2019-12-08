import json
import random

#Probabilities when generating a random output
prob_rate_like = 0.2
prob_rate_dislike = 0.8
assert (prob_rate_like + prob_rate_dislike) == 1

movies = []
directory = "output/dataset/"
with open(directory + "AllReviews_Reformatted_2_pruned.json", "r") as f:
    data = json.load(f)
    for movie in data:
        movie["Title"] = str.strip(movie["Title"][0])
        movies.append(movie)

score = -1
results = []
for movie in movies:
    #score = input(movie["Title"] + " like(1), dislike(2), or not seen (3) (q to quit) : ")

    #Use this to generate random ratings!
    rand = random.random()
    if rand < prob_rate_like: score = "1"
    else: score = "2"

    if score == "q":
        break
    movie_to_add = []
    movie_to_add.append(movie["Title"])
    movie_to_add.append(score)
    results.append(movie_to_add)

directory = "output/rated_movies/"
with open(directory + "Rand_Movie_Likes_and_Dislikes.json", "w") as f:
    json.dump(results, f)
# with open(directory + "Dylans_Movie_Data.json", "w") as f:
#         json.dump(results, f)