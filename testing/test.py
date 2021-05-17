import os
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class ezTreesTest(unittest.TestCase):

    def setUp(self):
        # get the path of ChromeDriverServer
        dir = os.path.dirname(__file__)
        self.driver = webdriver.Chrome(executable_path='drivers/chromedriver')

        # create a new Chrome session
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

        # Navigate to the application home page
        self.driver.get("http://127.0.0.1:5000/")


    def tearDown(self):
        if self.driver:
            self.driver.close()


    # test login with correct password
    def test_login_correct(self):
        #Giving login url to chrome driver
        self.driver.find_element_by_partial_link_text('Sign In').click()
        user_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit = self.driver.find_element_by_id('submit')

        #Filling username, password form and submit
        user_field.send_keys('michael')
        password_field.send_keys('admin')
        submit.click()

        #Check page redirects to Home after login
        title = self.driver.title
        self.assertIn(title, 'Home')


    # test login with incorrect password
    def test_login_incorrect(self):
        self.driver.find_element_by_partial_link_text('Sign In').click()
        user_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit = self.driver.find_element_by_id('submit')

        #Filling username, password form and submit
        user_field.send_keys('michael')
        password_field.send_keys('hacker9001')
        submit.click()

        #Check page doesn't redirect to Home after login
        title = self.driver.title
        self.assertNotIn(title, 'Home')


    # test quiz page redirect
    def test_loggedin_quiz_access(self):
        #Giving login url to chrome driver
        self.driver.find_element_by_partial_link_text('Sign In').click()
        user_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit = self.driver.find_element_by_id('submit')

        #Filling username, password form and submit
        user_field.send_keys('michael')
        password_field.send_keys('admin')
        submit.click()

        #Check redirection to quiz questions
        self.driver.find_element_by_partial_link_text('Quiz').click()
        title = self.driver.title
        self.assertIn(title, 'Quiz')

    # test content of content page
    def test_content(self):
        #navigate to content page
        self.driver.find_element_by_partial_link_text('Learn').click()
        title = self.driver.title
        self.assertIn(title, 'Learn')


if __name__ == '__main__':
    unittest.main()