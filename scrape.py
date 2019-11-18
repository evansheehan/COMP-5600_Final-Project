from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("http://www.imdb.com")
driver.implicitly_wait(5)

#Search movie
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("The Lighthouse")
elem.send_keys(Keys.RETURN)

#Click on first result
elem = driver.find_element_by_class_name("findResult.odd")
elem = elem.find_element_by_tag_name("a")
elem.click()

#Go to user reviews page
elem = driver.find_element_by_class_name("user-comments")
elem = elem.find_element_by_partial_link_text("user reviews")
elem.click()

wait = WebDriverWait(driver, 10)
while True:
    try:
        elem = driver.find_element_by_id("load-more-trigger")
        elem.click()
    except:
        break

reviews = driver.find_elements_by_class_name("imdb-user-review")

#driver.save_screenshot('screen.png')

print('No error')

driver.close()