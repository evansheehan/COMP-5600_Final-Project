import json

def rearrange_movie_list(movie_list):
    new_movie_list = []
    for movie in movie_list:
        new_movie = {
            "Title": movie["Title"],
            "Reviews": rearrange_review_dict(movie["Reviews"])
        }
        new_movie_list.append(new_movie)
    return new_movie_list

def rearrange_review_dict(review_list):
    if review_list == None:
        return None
    new_review_dict = {}
    for review_pair in review_list:
        review = {
            str(review_pair[1]): review_pair[0]
        }
        new_review_dict.update(review)
    return new_review_dict

def eliminate_empty_reviews(movie_list):
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

def generate_dicts(liked_movies, disliked_movies, liked_and_disliked_movies):
    liked_dict = {}
    disliked_dict = {}
    cumulative_dict = {}

    for movie in liked_movies:
        assert movie["Reviews"] != None, movie["Title"] + " has no reviews."
        reviews = list(movie["Reviews"].items())
        for review in reviews:
            word = review[0]
            count = review[1]
            if word in liked_dict:
                liked_dict[word] = liked_dict.get(word) + count
            else:
                liked_dict.update({word: count})

    for movie in disliked_movies:
        assert movie["Reviews"] != None, movie["Title"] + " has no reviews."
        reviews = list(movie["Reviews"].items())
        for review in reviews:
            word = review[0]
            count = review[1]
            if word in disliked_dict:
                disliked_dict[word] = disliked_dict.get(word) + count
            else:
                disliked_dict.update({word: count})

    for movie in liked_and_disliked_movies:
        assert movie["Reviews"] != None, movie["Title"] + " has no reviews."
        reviews = list(movie["Reviews"].items())
        for review in reviews:
            word = review[0]
            count = review[1]
            if word in cumulative_dict:
                cumulative_dict[word] = cumulative_dict.get(word) + count
            else:
                cumulative_dict.update({word: count})

    return liked_dict, disliked_dict, cumulative_dict