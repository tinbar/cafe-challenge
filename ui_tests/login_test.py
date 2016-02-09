import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_login(self):
        driver = self.driver
        driver.get("http://localhost:5000")
        login_button = driver.find_element_by_id('a-login')
        # Assert the login button is displayed to the user on this page
        self.assertTrue(login_button.is_displayed())
        # Click the button to go to the login page
        login_button.click()
        # Assert that the new url is the login page
        self.assertEqual(str(driver.current_url), 'http://localhost:5000/login')
        # Find user name field and assert it is displayed to user
        user_name_field = driver.find_element_by_id('user_name')
        self.assertTrue(user_name_field.is_displayed())
        # Find password field and assert it is displayed to user
        password_field = driver.find_element_by_id('password')
        self.assertTrue(password_field.is_displayed())
        # Fill user name and password with test data
        user_name_field.send_keys('jim')
        password_field.send_keys('jim')
        #password_field.send_keys(Keys.RETURN)
        # Submit
        submit_button = driver.find_element_by_id('button-login')
        submit_button.click()
        # The logout element should now be present after a successful login
        logout_button = driver.find_element_by_id('a-logout')
        self.assertTrue(logout_button.is_displayed())
        #elem = driver.find_element_by_name("q")
        #elem.send_keys("pycon")
        #elem.send_keys(Keys.RETURN)


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()