import json

all_movies = []
for i in range(2):
    with open("Iteration" + str(i) + ".json" ) as f:
        data = json.load(f)
        for movie in data:
            all_movies.append(movie)
            print("Stop")