import json
import numpy as np

LIKED_TRAINING_SET_SIZE = 200
DISLIKED_TRAINING_SET_SIZE = 100

liked_all = []
disliked_all = []
unseen = []

liked_training_set = []
disliked_training_set = []
liked_test_set = []
disliked_test_set = []

with open("Dylans_Movie_Data.json", "r") as f:
    data = json.load(f)
    for movie in data:
        if movie[1] == "1":
            liked_all.append(movie[0])
        elif movie[1] == "2":
            disliked_all.append(movie[0])

liked_training_set = np.random.choice(liked_all, LIKED_TRAINING_SET_SIZE, False)
disliked_training_set = np.random.choice(disliked_all, DISLIKED_TRAINING_SET_SIZE, False)

for movie in liked_all:
    if movie not in liked_training_set:
        liked_test_set.append(movie)

for movie in disliked_all:
    if movie not in disliked_training_set:
        disliked_test_set.append(movie)

with open("liked_training_set.json", "w") as f:
    json.dump(np.ndarray.tolist(liked_training_set), f)

with open("disliked_training_set.json", "w") as f:
    json.dump(np.ndarray.tolist(disliked_training_set), f)

with open("liked_test_set.json", "w") as f:
    json.dump(liked_test_set, f)

with open("disliked_test_set.json", "w") as f:
    json.dump(disliked_test_set, f)

