from wordcount import WordCount as wc
import string

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SEARCH_MOVIE = ""
LIKE_LIST = ["The Lighthouse", "Parasite", "Whiplash"]
DISLIKE_LIST = []

def getReviews(movieTitle):

    #Instantiate driver
    driver = webdriver.Chrome()
    driver.get("http://www.imdb.com")
    driver.implicitly_wait(1)

    #Search movie
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys(movieTitle)
    elem.send_keys(Keys.RETURN)

    #Click on first result
    elem = driver.find_element_by_class_name("findResult.odd")
    elem = elem.find_element_by_tag_name("a")
    elem.click()

    #Go to user reviews page
    elem = driver.find_element_by_class_name("user-comments")
    elem = elem.find_element_by_partial_link_text("user reviews")
    elem.click()

    #Continuously click the load more button until all reviews are loaded.
    #This works because of the implicit wait declared previously
    for i in range(10):
        try:
            elem = driver.find_element_by_id("load-more-trigger")
            elem.click()
        except:
            break

    reviewsList = driver.find_elements_by_class_name("imdb-user-review")
    reviews = ''

    #Currently ignores reviews with spoilers
    for review in reviewsList:
        reviewText = review.find_element_by_class_name("text").text
        if (reviewText != ''):
            #This add the current review text to one big string, reviews, making the string lowercase and getting rid of punctuation
            reviews += reviewText.lower().translate(str.maketrans('','',string.punctuation))
            #reviews.append(reviewText)
            print(reviewText)
            #review.find_element_by_class_name("spoiler-warning__control").click()
            #reviewText = review.find_element_by_class_name("text").text
        #print(reviewText)
        #reviews.append(reviewText)

    print(len(reviews))

    driver.close()

    return reviews

dictionary = dict
for movie in LIKE_LIST:
    dictionary = wc.countWords(wc, getReviews(movie))
    dictionary = wc.sortFreqDict(wc, dictionary)
    print('Stop')