from WordCount import WordCount as wc
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

def getReviews(movieTitle):

    #Instantiate driver
    driver = webdriver.Chrome()
    driver.get("http://www.imdb.com")
    wait = WebDriverWait(driver, 10)

    #Search movie
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys(movieTitle)
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
    """elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "user-comments"))):
    try:
        elem = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "user reviews")))
        elem.click()
    except:
        return"""
    while not EC.presence_of_element_located((By.CLASS_NAME, "user-comments")):
        driver.refresh()
    try:
        elem = driver.find_element_by_partial_link_text("user reviews")
        elem.click()
    except:
        driver.close()
        return None

    #Continuously click the load more button until all reviews are loaded.
    #This works because of the implicit wait declared previously
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
            #This adds the current review text to one big string, reviews, making the string lowercase and getting rid of punctuation
            #reviews += reviewText.lower().translate(str.maketrans('','',string.punctuation))

            review.find_element_by_class_name("spoiler-warning__control").click()
            reviewText = review.find_element_by_class_name("text").text
            reviews += reviewText.lower().translate(str.maketrans('','',string.punctuation))

        print(reviewText)

    print(len(reviews))

    driver.close()

    return reviews

def generateDict(reviewList):
    dictionary = wc.countWords(wc, reviewList)
    dictionary = wc.sortFreqDict(wc, dictionary)
    return dictionary

like_dict = generateDict(LIKE_LIST)
with open("Dislike_List.json", 'w') as f:
        json.dump(like_dict, f)

dislike_dict = generateDict(DISLIKE_LIST)
with open("Like_List.json", 'w') as f:
        json.dump(like_dict, f)

print('Stop')