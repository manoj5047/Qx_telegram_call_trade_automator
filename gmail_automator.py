from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import json

import undetected_chromedriver as uc
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



# First Script: Extract Authorization Session ID
options = uc.ChromeOptions()
options.add_experimental_option('w3c', True)
options.add_argument('--disable-extensions')
options.add_argument('--disable-infobars')
options.add_argument('--disable-popup-blocking')
options.add_argument('--start-maximized')
options.add_argument('--disable-notifications')
options.add_argument('--disable-gpu')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-notifications")

capabilities = DesiredCapabilities.CHROME.copy()
capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
capabilities['perfLoggingPrefs'] = {'enableNetwork': True, 'enablePage': False}
driver = uc.Chrome(options=options, capabilities=capabilities)
# Launch a web browser

# Navigate to the webpage that requires OTP verification
# driver.get("https://www.example.com/otp_verification")
#
# # Enter your Gmail credentials
# email_field = driver.find_element_by_name("email")
# email_field.send_keys("your_email@gmail.com")
# password_field = driver.find_element_by_name("password")
# password_field.send_keys("your_password")
# password_field.send_keys(Keys.RETURN)

# Wait for the OTP email to arrive
# time.sleep(10)

# Log in to your Gmail account
driver.get("https://mail.google.com/")
email_field = driver.find_element_by_name("identifier")
email_field.send_keys("smj31071995@gmail.com")
email_field.send_keys(Keys.RETURN)
time.sleep(5)
password_field = driver.find_element_by_name("password")
password_field.send_keys("Pas$w06D@Gmail")
password_field.send_keys(Keys.RETURN)

# Extract the OTP code from the email message
time.sleep(5)
otp_email = driver.find_element_by_xpath("//span[contains(text(), 'Your OTP code is:')]/..")
otp_code = otp_email.text.split()[-1]

# Fill in the OTP field on the webpage
otp_field = driver.find_element_by_name("otp")
otp_field.send_keys(otp_code)

# Submit the form and complete the verification process
submit_button = driver.find_element_by_name("submit")
submit_button.click()
