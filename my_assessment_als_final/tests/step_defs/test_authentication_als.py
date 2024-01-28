"""
This module contains step definitions for authentication_als.feature.
It uses Selenium WebDriver for browser interactions:
https://www.seleniumhq.org/projects/webdriver/
Setup and cleanup are handled using hooks.

"""

import time
from pytest_bdd import scenarios, when, then, parsers
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

timeoutSmall = 10

# Scenarios

scenarios('../features/authentication_als.feature')


# When Steps

# The user inserts text into text field using ID for locating
@when(parsers.parse('the user inserts "{text}" to "{locator}"'))
def insert_my_text(browser, text, locator):
    time.sleep(1)
    if(text != "noValue"):
        WebDriverWait(browser, timeoutSmall).until(
            EC.presence_of_element_located((By.ID, locator))).send_keys(text)
    time.sleep(3)

# The user clicks a button using ID for locating
@when(parsers.parse('press button by id "{name}"'))
def press_btn_by_id(browser, name):
    WebDriverWait(browser, timeoutSmall).until(
        EC.element_to_be_clickable((By.ID, name))).click()
    time.sleep(5)


# Then Steps

# Checking if the products page is loaded, or in error case check if error message appears and verify that matches
@then(parsers.parse('wait for products page to be loaded "{errorCase}" or "{myMsg}"'))
def products_page_manipulation(browser, errorCase, myMsg):
    # if(errCase != "0"):
    if(int(errorCase)):
        time.sleep(5)
        browser.find_element(By.XPATH, "//div[contains(@class, 'error-message-container')]")
        WebDriverWait(browser, timeoutSmall).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'error-message-container')]"))).is_displayed()
        errorTxt = browser.find_element(By.XPATH, "//div[contains(@class, 'error-message-container')]/h3").text
        assert errorTxt == myMsg
    else:
        # Trying to verify a correct load of the page of products and checks in parallel the header text to be Products
        time.sleep(5)
        WebDriverWait(browser, timeoutSmall).until(
            EC.presence_of_element_located((By.ID, "inventory_container"))).is_displayed()
        headerTxt = browser.find_element(By.XPATH, "//*[@id='header_container']/div[2]/span").text
        assert headerTxt == "Products"