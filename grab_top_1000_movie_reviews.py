import json
import sys
import scrape
#from MovieObj import Movie

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

ITERATION_SIZE = 50

movie_titles = []
movies = []

with open("Top1000.json", "r") as f:
    movie_titles = json.load(f)

#with open("MoviesAndReviews.json", "a") as f:
#json.dump([], f)
#divideTitles = int(len(movieTitles)/20)
iteration = 16

try:
    if open("Iteration" + str(iteration) + ".json"):
        response = input("File already exists, would you like to replace it? y or n:")
        if response == "n":
                sys.exit("File already exists, don't replace.")
        while response not in ["y", "n"]:
            response = input("Please input a y or n:")
            if response == "n":
                sys.exit("File already exists, don't replace.")
            elif response == "y":
                break
except FileNotFoundError:
    print("File not found...a new one will be created")

try:
    current_index = 1+movie_titles.index("Pet Sematary (2019)")
except:
    sys.exit("Cannot find index of given movie")

print(current_index)

for i in range(current_index, 1000):
    try:
        movie_title = movie_titles[i]
        movie_title = movie_title.split("(")
        #reviews = Scrape.getReviews(movieTitle[0])
        
        """if reviews != None:
            reviewDict = Scrape.generateDict(reviews)
        else:
            reviewDict = None

        movie = {
            "Title": movieTitle,
            "Reviews": reviewDict
        }"""

        movie = Scrape.generate_movie(movie_title[0])
        movies.append(movie)
        
    except:
        break

with open("Iteration" + str(iteration) + ".json", "w") as f:
    json.dump(movies, f)
    

