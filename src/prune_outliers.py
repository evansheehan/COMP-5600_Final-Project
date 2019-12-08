import json
import numpy as np

def prune_outliers(movies):
    unique_words = []
    out_array = []

    for movie in movies:
        if movie["Reviews"] != None:
            unique_words.append(len(movie["Reviews"]))

    std_dev = np.std(unique_words)
    mean = np.mean(unique_words)

    minimum = 0#mean - std_dev
    maximum = 9999#mean + std_dev

    unpruned_data = []
    directory = "output/rated_movies/"
    file_name = "Dylans_Movie_Data"
    with open(directory + file_name + ".json", "r") as f: 
        data = json.load(f)
        for movie in movies:
            if movie["Reviews"] != None:
                if len(movie["Reviews"]) in range(int(minimum), int(maximum)):
                    out_array.append(movie)
                    for d_movie in data:
                        if d_movie[0] == str.strip(movie["Title"][0]):
                            unpruned_data.append(d_movie)
                else:
                    print(movie["Title"][0] + " removed because it was outside std dev: " + str(len(movie["Reviews"])))

            else:
                print(movie["Title"][0] + " removed because it had no reviews")

    print(str(len(unpruned_data)))

    with open(directory + file_name + "_pruned.json", "w") as f:
        json.dump(unpruned_data, f)

    print(len(movies) - len(out_array))
    return out_array

pruned_data = []
directory = "output/dataset/"
file_name = "AllReviews_Reformatted_2"
with open(directory + file_name + ".json", "r") as f: 
    data = json.load(f)
    pruned_data = prune_outliers(data)

with open(directory + file_name + "_pruned.json", "w") as f:
    json.dump(pruned_data, f)
