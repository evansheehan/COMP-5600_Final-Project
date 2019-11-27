import json
import Scrape
from MovieObj import Movie

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

movieTitles = []
movies = []

with open("Top1000.json", "r") as f:
    movieTitles = json.load(f)

for movieTitle in movieTitles:
    reviews = Scrape.getReviews(movieTitle)
    reviewDict = Scrape.generateDict(reviews)
    movie = Movie(movieTitle, reviewDict)
    movies.append(movie)

with open("MoviesAndReviews", "w") as f:
    json.dump(movies, f)
    

