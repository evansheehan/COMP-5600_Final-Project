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

    minimum = mean - std_dev
    maximum = mean + 2*std_dev

    for movie in movies:
        if movie["Reviews"] != None:
            if len(movie["Reviews"]) in range(int(minimum), int(maximum)):
                out_array.append(movie)
            else:
                print(movie["Title"][0] + " removed because it was outside std dev: " + str(len(movie["Reviews"])))

        else:
            print(movie["Title"][0] + " removed because it had no reviews")

    print(len(movies) - len(out_array))
    return out_array


pruned_data = []
file_name = "Dylans_Movie_Data"
with open(file_name + ".json", "r") as f: 
    data = json.load(f)
    pruned_data = prune_outliers(data)

with open(file_name + "_pruned.json", "w") as f:
    json.dump(pruned_data, f)

pruned_data = []
file_name = "AllReviews_Reformatted_2"
with open(file_name + ".json", "r") as f: 
    data = json.load(f)
    pruned_data = prune_outliers(data)

with open(file_name + "_pruned.json", "w") as f:
    json.dump(pruned_data, f)

print("test")