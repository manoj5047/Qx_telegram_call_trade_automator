import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

opt = webdriver.ChromeOptions()
opt.add_experimental_option('w3c', True)
opt.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(chrome_options=opt, desired_capabilities={
    'loggingPrefs': {'performance': 'ALL'}})
driver.delete_all_cookies()
driver.get("https://quotex.io/en/sign-in/")
ssid = None
while True:
    if ssid != None:
        break

    for entry in driver.get_log('browser'):
        start_send = False
        try:
            shell = entry["message"]
            payloadData = json.loads(
                shell)["message"]["params"]["response"]["payloadData"]

            if "authorization" in shell and "session" in shell:
                ssid = payloadData
                print(ssid)
        except:
            pass
