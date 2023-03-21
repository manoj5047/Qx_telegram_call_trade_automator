import datetime
import json

import undetected_chromedriver as uc
from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Find the Up and Down buttons inside the section-deal div
up_button = None
down_button = None
amount_text_field = None
time_set_button = None
add_input_element = None
remove_input_element = None
default_amount = 1  # Dollars
default_time = 5  # Minutes
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


def start_driver():
    driver.delete_all_cookies()
    WebDriverWait(driver, 20)
    driver.get("https://quotex.io/en/sign-in/")


def open_gmail():
    driver.delete_all_cookies()
    WebDriverWait(driver, 20)
    driver.get("https://quotex.io/en/sign-in/")


def login_flow_script():
    do_login()
    print("Logged in successfully. Current URL: " + driver.current_url)

    switch_to_demo_trade()
    print("Switched to demo trade")

    find_dash_board_buttons()
    print("Found Buttons")

    setup_input_buttons()
    print("Found Input Buttons")

    place_long_order(is_to_place_order=False, miutes=0, amount=1)
    place_short_order(is_to_place_order=False, miutes=0, amount=1)


def do_login():
    # Enter email and password
    email = "smj31071995@gmail.com"
    password = "Pas$w06D@Qx"
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)

    # Click Sign In button
    driver.find_element(By.CLASS_NAME, "modal-sign__block-button").click()

    # Wait for the dashboard to load
    WebDriverWait(driver, 60).until(expected_conditions.url_contains('trade'))


def switch_to_demo_trade():
    # Change trade to demo trade
    driver.find_element(By.CLASS_NAME, "usermenu").click()
    driver.find_element(By.XPATH, "//a[@href='https://qxbroker.com/en/demo-trade']").click()


def get_future_time(minutes):
    # get the current time
    now = datetime.datetime.now()
    print(f'current time {now.strftime("%H:%M")}')

    # add 5 minutes to the current time
    future_time = now + datetime.timedelta(minutes=minutes)

    # format the future time in HH:MM format
    future_time_str = future_time.strftime('%H:%M')

    # return the future time in HH:MM format
    return future_time_str


def find_dash_board_buttons():
    global down_button, up_button, amount_text_field, time_set_button, remove_input_element, add_input_element
    try:
        down_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".section-deal__danger")))

    except TimeoutException:
        print("Timed out waiting for DOWN to be visible")
    try:
        up_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".section-deal__success")))
    except TimeoutException:
        print("Timed out waiting for UP to be visible")
    try:
        amount_text_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.section-deal__investment '
                                                               'input.input-control__input[type="text"]')))
        value = amount_text_field.get_attribute("value")
        print(f"AMOUNT TEXT FIELD VALUE : {value}")
    except TimeoutException:
        # handle timeout exception here
        print("Timed out waiting for amount_text_field to be visible")
    try:
        time_set_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(@class, 'input-control__label') and text()='Time']")))
    except TimeoutException:
        # handle timeout exception here
        print("Timed out waiting for time_set_button to be visible")
    try:
        remove_input_element = driver.find_element(By.XPATH,
                                                   "//button[contains(@class, 'input-control__button') and text()='-']")

        add_input_element = driver.find_element(By.XPATH,
                                                "//button[contains(@class, 'input-control__button') and text()='+']")
    except Exception:
        print("ERROR on + and - Buttons findings")


# Click on the Up button
def place_long_order(is_to_place_order, miutes, amount):
    if up_button is not None:
        if is_to_place_order is False:
            print("UP AVAILABLE")
        else:
            setup_amount(amount)
            setup_time(minutes=miutes)
            up_button.click()
    else:
        print("Up element not found yet")


# Click on the Down button
def place_short_order(is_to_place_order, miutes, amount):
    if down_button is not None:
        if is_to_place_order is False:
            print("DOWN AVAILABLE")
        else:
            setup_amount(amount)
            setup_time(minutes=miutes)
            down_button.click()
    else:
        print("Down element not found yet")


def setup_currency():
    xpath_for_currency_btn = "//div[contains(@class, 'tab desktop')']"
    # currency_


def setup_input_buttons():
    if amount_text_field is not None:
        print("AMOUNT AVAILABLE")
        setup_time(default_time)
        setup_amount(default_amount)
        # setup_currency()
    else:
        print("AMOUNT NOT AVAILABLE")


def setup_time(minutes):
    print(get_future_time(1 if minutes <= 0 else minutes))
    time_set_button.click()
    xpath = f"//div[contains(@class, 'input-control__dropdown-option') and text()='{get_future_time(minutes)}']"
    print(xpath)
    future_time_button = driver.find_element(By.XPATH, xpath)
    # Move the mouse cursor to the button and click it
    action_chains = ActionChains(driver)
    action_chains.move_to_element(future_time_button).click().perform()
    # future_time_button.click()


def setup_amount(amount):
    amount_text_field.click()
    value = amount_text_field.get_attribute("value")
    print(f'before value {value}')

    if amount <= 1:
        amount_text_field.clear();
    elif amount > 1:
        amount_text_field.send_keys(amount)
    value = amount_text_field.get_attribute("value")
    print(f'after value {value}')
    # final_value = int(value.replace('$', ''))
    # for i in range(final_value, 0, -1):
    #     remove_input_element.click()
    #     print(amount_text_field.get_attribute("value").replace("$", ""))


def keep_in_loop_till_find_ssid():
    ssid = None
    while True:
        if ssid != None:
            break

        for entry in driver.get_log('driver'):
            # Your code here
            start_send = False
            try:
                shell = entry["message"]
                print(shell)

                payloadData = json.loads(shell)["message"]["params"]["response"]["payloadData"]
                if "authorization" in shell and "session" in shell:
                    ssid = payloadData
                    print("Authorization Session ID: " + ssid)
            except:
                pass


# keep_in_loop_till_find_ssid()


def closeBrowser():
    # Close the browser
    driver.quit()
