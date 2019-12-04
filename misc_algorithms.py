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

movie_list = []

with open("AllReviews.json", "r") as f:
    movie_list = json.load(f)
    movie_list = rearrangeMovieList(movie_list)
    print("debug")

with open("AllReviews_Reformatted.json", "w") as f:
    json.dump(movie_list, f)