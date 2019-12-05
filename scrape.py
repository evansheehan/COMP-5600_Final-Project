from word_count import WordCount as wc
import string
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LIKE_LIST = ["Avengers End", "The Terminator", "The Matrix"]
DISLIKE_LIST = ["It Chapter 2", "The Shining", "Doctor Sleep"]

like_dict = dict
dislike_dict = dict

def get_reviews(movie_title):

    #Instantiate driver
    driver = webdriver.Chrome()
    driver.get("http://www.imdb.com")
    wait = WebDriverWait(driver, 10)

    #Search movie
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys(movie_title)
    elem.send_keys(Keys.RETURN)

    #Click on first result
    while not EC.presence_of_element_located((By.CLASS_NAME, "findResult.odd")):
        driver.refresh()
    #elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "findResult.odd")))
    elem = driver.find_element_by_class_name("findResult.odd")

    #elem = driver.find_element_by_class_name("findResult.odd")
    #elem = wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))
    elem = elem.find_element_by_tag_name("a")
    try:
        elem.click()
    except:
        return None

    #Go to user reviews page
    while not EC.presence_of_element_located((By.CLASS_NAME, "user-comments")):
        driver.refresh()
    try:
        elem = driver.find_element_by_partial_link_text("user reviews")
        elem.click()
    except:
        driver.close()
        return None

    #Continuously click the load more button until all reviews are loaded.
    for i in range(4):
        try:
            elem = wait.until(EC.presence_of_element_located((By.ID, "load-more-trigger")))
            elem.click()
        except:
            break
    reviewsList = driver.find_elements_by_class_name("imdb-user-review")
    reviews = ''

    #Currently ignores reviews with spoilers
    for review in reviewsList:
        reviewText = review.find_element_by_class_name("text").text
        if (reviewText == ''):
            review.find_element_by_class_name("spoiler-warning__control").click()
            reviewText = review.find_element_by_class_name("text").text
            reviews += reviewText.lower().translate(str.maketrans('','',string.punctuation))
        print(reviewText)

    print(len(reviews))

    driver.close()

    return reviews

def generate_dict(reviewList):
    dictionary = wc.countWords(wc, reviewList)
    dictionary = wc.sortFreqDict(wc, dictionary)
    return dictionary

def generate_movie(movie_title):
    reviews = get_reviews(movie_title)
    if reviews != None:
        review_dictionary = generate_dict(reviews)
    else:
        review_dictionary = None
    movie = {
        "Title": movie_title,
        "Reviews": review_dictionary
    }
    return movie

like_dict = generate_dict(LIKE_LIST)
with open("Dislike_List.json", 'w') as f:
        json.dump(like_dict, f)

dislike_dict = generate_dict(DISLIKE_LIST)
with open("Like_List.json", 'w') as f:
        json.dump(like_dict, f)

print('Stop')