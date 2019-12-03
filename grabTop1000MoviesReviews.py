import json
import Scrape
#from MovieObj import Movie

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

ITERATION_SIZE = 25

movieTitles = []
movies = []

with open("Top1000.json", "r") as f:
    movieTitles = json.load(f)

#with open("MoviesAndReviews.json", "a") as f:
#json.dump([], f)
#divideTitles = int(len(movieTitles)/20)
iteration = 2

for i in range(iteration*ITERATION_SIZE, ITERATION_SIZE+(iteration*ITERATION_SIZE)):
    movieTitle = movieTitles[i]
    movieTitle = movieTitle.split("(")
    reviews = Scrape.getReviews(movieTitle[0])
    
    if reviews != None:
        reviewDict = Scrape.generateDict(reviews)
        #movie = Movie(movieTitle, reviewDict)
    else:
        reviewDict = None
        #movie = Movie(movieTitle, None)

    movie = {
        "Title": movieTitle,
        "Reviews": reviewDict
    }

    movies.append(movie)

with open("Iteration" + str(iteration) + ".json", "w") as f:
    json.dump(movies, f)


"""with open("MoviesAndReviews", "w") as f:
    json.dump(movies, f)"""
    

