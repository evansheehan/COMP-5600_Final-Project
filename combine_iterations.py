import json

all_movies = []
for i in range(17):
    with open("Iteration" + str(i) + ".json" ) as f:
        data = json.load(f)
        for movie in data:
            all_movies.append(movie)
            #print("Stop")

try:
    assert len(all_movies) == 1000
except AssertionError:
    print("Size of all_movies list is: " + str(len(all_movies)))

with open("AllReviews.json", "w") as f:
    json.dump(all_movies, f)