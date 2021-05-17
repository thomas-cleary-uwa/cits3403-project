import os
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
import time

# get the path of ChromeDriverServer
dir = os.path.dirname(__file__)
driver = webdriver.Chrome(executable_path='drivers/chromedriver')

# create a new Chrome session
driver.implicitly_wait(5)
driver.maximize_window()

# Navigate to the application home page
driver.get("http://127.0.0.1:5000/")

x = driver.find_element_by_partial_link_text('Sign')
x.click()

time.sleep(10)




# close the browser window
driver.quit()