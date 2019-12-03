import json

class Movie:
    movieTitle = str
    movieReviews = dict

    def __init__(self, titleIn, reviewsIn):
        movieTitle = json.dumps(titleIn)
        movieReviews = json.dumps(reviewsIn)