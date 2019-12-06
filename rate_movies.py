import json
import random

movies = []
with open("AllReviews_Reformatted_2.json") as f:
    data = json.load(f)
    for movie in data:
        movie["Title"] = str.strip(movie["Title"][0])
        movies.append(movie)

score = -1
results = []
for movie in movies:
    #score = input(movie["Title"] + " like(1), dislike(2), or not seen (3) (q to quit) : ")
    score = str(random.randrange(1, 3))
    if score == "q":
        break
    movie_to_add = []
    movie_to_add.append(movie["Title"])
    movie_to_add.append(score)
    results.append(movie_to_add)


with open("Rand_Movie_Likes_and_Dislikes.json", "w") as f:
    json.dump(results, f)
# with open("Dylans_Movie_Data.json", 'w') as f:
#         json.dump(results, f)