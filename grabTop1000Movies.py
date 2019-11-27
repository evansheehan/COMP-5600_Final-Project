import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

popular1000 = []

#Instantiate driver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

def process_movie_titles(movieList):
    if len(movieList) == 0:
        return
    for movie in movieList:
        movieTitle = movie.string
        popular1000.append(movieTitle)

pageNum = 1
while len(popular1000) < 1000:
    driver.get("https://letterboxd.com/films/popular/size/small/page/" + str(pageNum))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "poster-container")))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    titleElems = soup.find_all("span", class_="frame-title")
    process_movie_titles(titleElems)
    print("Iteration " + str(pageNum) + "...list size is " + str(len(popular1000)))
    pageNum += 1
    if len(popular1000) == 0:
        print("List did not populate")  
        break

if len(popular1000) != 0:
    with open("Top1000.json", "w") as f:
        json.dump(popular1000, f)

driver.close()