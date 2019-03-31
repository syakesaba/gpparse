#!/usr/local/bin/python3
# encoding: utf-8

import os
import json
import time
import logging
logging.basicConfig(level=logging.INFO)

from selenium.webdriver import Remote
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

USERDATA_DIR = "/tmp/chronium" #chrome:/tmp/chronium #save session/cache files
CURDIR = os.path.dirname(os.path.abspath(__file__))

CHRONIUM_ARGS = [
    #"--proxy-bypass-list",
    #"--proxy-pac-url",
    #"--proxy-server",
    "--user-data-dir=%s" % USERDATA_DIR,
    "--ignore-certificate-errors",
    "--lang=ja"
]

GOOGLE_USER = None
GOOGLE_PASS = None
ACCOUNT_FILE = os.path.join(CURDIR, "account.json")

with open(ACCOUNT_FILE) as f:
    account = json.load(f)
    GOOGLE_USER = account["GOOGLE_ID"]
    GOOGLE_PASS = account["GOOGLE_PASS"]

def setupBrowser():
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:chromeOptions"] = {"args":CHRONIUM_ARGS}
    driver = Remote(
        command_executor='http://selenium-hub-gpparse:4444/wd/hub',
        desired_capabilities=desired_capabilities
    )
    browser = driver
    browser.implicitly_wait(3) #seconds
    browser.maximize_window()
    return browser

def login(browser):
    browser.get("https://accounts.google.com/signin/v2/identifier")
    time.sleep(3)
    if "ログイン" in browser.title:
        print("Not Logged In")
        WebDriverWait(browser, 10).until( #seconds
            expected_conditions.visibility_of_element_located((By.NAME, 'identifier'))
        )
        idTextBox = browser.find_element_by_name('identifier')
        idTextBox.send_keys(GOOGLE_USER)
        idTextBox.send_keys(Keys.RETURN)
        WebDriverWait(browser, 10).until( #seconds
          expected_conditions.visibility_of_element_located((By.NAME, 'password'))
        )
        passwordTextBox = browser.find_element_by_name('password')
        passwordTextBox.send_keys(GOOGLE_PASS)
        passwordTextBox.send_keys(Keys.RETURN)
        WebDriverWait(browser, 10).until( #seconds
          expected_conditions.visibility_of_element_located((By.TAG_NAME, 'body'))
        )
    time.sleep(3)
    print(browser.title)

def printlinks(browser):
    with open("links.txt") as f:
        for line in f:
            time.sleep(1)
            link = line.strip()
            print(link)
            browser.get(link)
            WebDriverWait(browser, 10).until( #seconds
              expected_conditions.visibility_of_element_located((By.TAG_NAME, 'body'))
            )
            # Ref: https://stackoverflow.com/a/52572919/
            original_size = browser.get_window_size()
            required_width = browser.execute_script('return document.body.parentNode.scrollWidth')
            required_height = browser.execute_script('return document.body.parentNode.scrollHeight')
            browser.set_window_size(required_width, required_height)
            element = browser.find_element_by_tag_name("body")
            element_text = element.text
            element_png = element.screenshot_as_png
            browser.set_window_size(original_size['width'], original_size['height'])
            filename=link.replace(":","_").replace("/","_")
            with open(filename + ".png", "wb") as fp:
                fp.write(element_png)
            with open(filename + ".txt", "w", encoding='utf-8') as fp:
                fp.write(element_text)

try:
    browser = setupBrowser()
    login(browser)
    #checkLogin(browser)
    printlinks(browser)
    browser.quit()
except Exception as e:
    browser.quit()
    print(e)
