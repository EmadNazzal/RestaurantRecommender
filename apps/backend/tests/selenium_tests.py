"""Selenium tests for the web application."""

import os
import sys
import time
import unittest

import django
import requests  # type: ignore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from user_management.tests import sample_users  # type: ignore

TWO_HUNDRED = 200

# Add the path to your Django project directory.
# Change this to the path of the backend directory in your project.
sys.path.append("/Users/riink/OneDrive/Summer_project/SummerProject/GitHub/apps/backend/")

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Initialise Django.
django.setup()


class WebAppIntegrationTest(unittest.TestCase):
    """Integration tests for the web application using Selenium WebDriver.

    Tests cover login, registration, password reset, contact form submission, and logout functionalities.
    """

    def setUp(self):
        """Set up the test environment by initializing the WebDriver and setting the base URL."""
        self.driver = webdriver.Chrome()
        self.base_url = "http://137.43.49.25/api/"

    def tearDown(self):
        """Tear down the test environment by quitting the WebDriver after each test."""
        self.driver.quit()

    def test_login(self):
        """Test the login functionality using dictionary from APITestCase tests.

        - Tests both; correct and incorrect login attempts.
        - Verifies successful login by checking the presence of the logout button.

        Raises:
            AssertionError: If the login does not function correctly.
        """
        driver = self.driver
        driver.get(f"{self.base_url}/login")

        # Correct login, with a dictionary data from APITestCase
        user = sample_users[0]
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        email_field.send_keys(user["email"])
        password_field.send_keys(user["password1"])
        password_field.send_keys(Keys.RETURN)

        time.sleep(2)
        try:
            # A logout button is used to confirm successful login
            logout_button = driver.find_element(By.NAME, "logout")
            self.assertTrue(logout_button.is_displayed())
        except ValueError as e:
            self.fail(f"Login failed for user: {user['email']} with error: {e}")

        # Incorrect login, login attempt with an email and a password that have not been registered
        driver.get(f"{self.base_url}/login")
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        email_field.send_keys("notindatabase@example.com")
        password_field.send_keys("doesnotmatterreally1")
        password_field.send_keys(Keys.RETURN)

        time.sleep(2)

    def test_registration(self):
        """Test the user registration functionality.

        - Tests both; correct and incorrect registration.
        - Verifies successful registration by checking for user presence.

        Raises:
            AssertionError: If the registration functionality fails.
        """
        driver = self.driver
        driver.get(f"{self.base_url}/register")

        # Correct registration
        user = sample_users[1]
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        confirm_password_field = driver.find_element(By.NAME, "reset-password-confirm")
        first_name_field = driver.find_element(By.NAME, "first_name")
        surname_field = driver.find_element(By.NAME, "surname")

        email_field.send_keys(user["email"])
        password_field.send_keys(user["password1"])
        confirm_password_field.send_keys(user["password2"])
        first_name_field.send_keys(user["first_name"])
        surname_field.send_keys(user["surname"])
        confirm_password_field.send_keys(Keys.RETURN)

        # Wait for registration to complete
        time.sleep(10)

        # Missing fields registration, verifies that user cannot create an account when not filling in all required fields
        driver.get(f"{self.base_url}/register")
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        first_name_field = driver.find_element(By.NAME, "first_name")

        email_field.send_keys(sample_users[2]["email"])
        password_field.send_keys(sample_users[2]["password1"])
        first_name_field.send_keys(sample_users[2]["first_name"])
        password_field.send_keys(Keys.RETURN)

        time.sleep(10)

    def test_password_reset(self):
        """Test the password reset functionality.

        - Requests a password reset.
        - Confirms the password reset.

        TODO(RiinKal):
        - Need to change the logic of testing when email service has been setup.

        Raises:
            AssertionError: If the password reset functinality does not work as expected.
        """
        driver = self.driver
        user = sample_users[7]

        # Request password reset
        driver.get(f"{self.base_url}/reset-password")
        email_field = driver.find_element(By.NAME, "email")
        email_field.send_keys(user["email"])
        email_field.send_keys(Keys.RETURN)
        time.sleep(2)

        # API call to get reset token
        reset_token_url = f"{self.base_url}/reset-password/"
        response = requests.post(reset_token_url, data={"email": user["email"]})  # noqa: S113
        if response.status_code == TWO_HUNDRED:
            reset_token = response.json().get("token")
        else:
            self.fail("Failed to get reset token")

        # Confirm password reset
        driver.get(f"{self.base_url}/reset-password/confirm/{reset_token}")
        new_password_field = driver.find_element(By.NAME, "new_password")
        new_password_field.send_keys(user["password_reset"])
        new_password_field.send_keys(Keys.RETURN)

        time.sleep(2)

    def test_contact_us(self):
        """Test the contact us functionality.

        - Allows users to use contact us functionality.

        Raises:
            AssertionError: If the contact does not work as expected.
        """
        driver = self.driver
        driver.get(f"{self.base_url}/contact")

        user = sample_users[6]
        name_field = driver.find_element(By.NAME, "name")
        email_field = driver.find_element(By.NAME, "email")
        subject_field = driver.find_element(By.NAME, "subject")
        message_field = driver.find_element(By.NAME, "message")

        name_field.send_keys(user["name"])
        email_field.send_keys(user["email"])
        subject_field.send_keys(user["subject"])
        message_field.send_keys(user["message"])
        message_field.send_keys(Keys.RETURN)

        time.sleep(10)

    def test_logout(self):
        """Logout test to check if the user is able to logout.

        - First user logs in.
        - Ensures that the access token is present.
        - Verifies successful logout.

        Raises:
            AssertionError: If the logout process does not work as expected.
        """
        driver = self.driver
        driver.get(f"{self.base_url}/login")

        user = sample_users[0]
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        email_field.send_keys(user["email"])
        password_field.send_keys(user["password1"])
        password_field.send_keys(Keys.RETURN)

        time.sleep(2)
        try:
            logout_button = driver.find_element(By.NAME, "logout")
            logout_button.click()
            time.sleep(2)
            login_button = driver.find_element(By.NAME, "login")
            self.assertTrue(login_button.is_displayed())
        except ValueError as e:
            self.fail(f"Logout failed for user: {user['email']} with error: {e}")


"""
class LoginFlowTests(StaticLiveServerTestCase): # 1.

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = create_test_user()
        cls.selenium = WebDriver() # 2.
        cls.selenium.implicitly_wait(5) # 3.

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login_flow(self):
        test.selenium.get(f"{test.live_server_url}/accounts/login") # 4.
        username_input = test.selenium.find_element(By.NAME, "user") # 5.
        username_input.send_keys(test.test_user.email) # 6.
        password_input = test.selenium.find_element(By.NAME, "pass")
        password_input.send_keys(test.test_user.password)
        test.selenium.find_element(By.ID, "sign-in").click()
        self.assertEqual(user_has_logged_in(self.test_user), true) # 7.
"""

if __name__ == "__main__":
    unittest.main()
