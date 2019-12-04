import json

def rearrangeMovieList(movie_list):
    new_movie_list = []
    for movie in movie_list:
        new_movie = {
            "Title": movie["Title"],
            "Reviews": rearrangeReviewDict(movie["Reviews"])
        }
        new_movie_list.append(new_movie)
    return new_movie_list

def rearrangeReviewDict(review_list):
    if review_list == None:
        return None
    new_review_dict = {}
    for review_pair in review_list:
        review = {
            str(review_pair[1]): review_pair[0]
        }
        new_review_dict.update(review)
    return new_review_dict

def eliminateEmptyReviews(movie_list):
    new_movie_list = []
    for movie in movie_list:
        try:
            if len(movie["Reviews"]) == 0:
                movie["Reviews"] = None
                print(movie["Title"][0] + " had no reviews...set to None")
        except:
            movie = {
                "Title": movie["Title"],
                "Reviews": None
            }
        new_movie_list.append(movie)

    return new_movie_list

movie_list = []

with open("AllReviews_Reformatted.json", "r") as f:
    movie_list = json.load(f)
    movie_list = eliminateEmptyReviews(movie_list)
    print("debug")

with open("AllReviews_Reformatted_2.json", "w") as f:
    json.dump(movie_list, f)