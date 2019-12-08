import json
import numpy as np

def reset_data(liked_set_ratio_in, disliked_set_ratio_in):

    liked_training_set_size = liked_set_ratio_in
    disliked_training_set_size = disliked_set_ratio_in

    liked_all = []
    disliked_all = []
    unseen = []

    liked_training_set = []
    disliked_training_set = []
    liked_test_set = []
    disliked_test_set = []

    directory = "output/rated_movies/"
    file_name = "Dylans_Movie_Data_pruned.json"
    # file_name = "Rand_Movie_Likes_and_Dislikes.json"

    with open(directory + file_name, "r") as f:
        data = json.load(f)
        for movie in data:
            if movie[1] == "1":
                liked_all.append(movie[0])
            elif movie[1] == "2":
                disliked_all.append(movie[0])

    print(file_name + " being used to generate training and test set.")
    liked_training_set_size *= len(liked_all)
    liked_training_set_size = int(liked_training_set_size)
    disliked_training_set_size *= len(disliked_all)
    disliked_training_set_size = int(disliked_training_set_size)

    liked_training_set = np.random.choice(liked_all, liked_training_set_size, False)
    disliked_training_set = np.random.choice(disliked_all, disliked_training_set_size, False)

    for movie in liked_all:
        if movie not in liked_training_set:
            liked_test_set.append(movie)

    for movie in disliked_all:
        if movie not in disliked_training_set:
            disliked_test_set.append(movie)

    directory = "output/generated_sets/"
    with open(directory + "liked_training_set.json", "w") as f:
        json.dump(np.ndarray.tolist(liked_training_set), f)

    with open(directory + "disliked_training_set.json", "w") as f:
        json.dump(np.ndarray.tolist(disliked_training_set), f)

    with open(directory + "liked_test_set.json", "w") as f:
        json.dump(liked_test_set, f)

    with open(directory + "disliked_test_set.json", "w") as f:
        json.dump(disliked_test_set, f)

    return liked_training_set_size/len(liked_all), disliked_training_set_size/len(disliked_all)
