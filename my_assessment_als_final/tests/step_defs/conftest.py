import pytest
import time

from pytest_bdd import given, when, parsers
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# Constants

MAIN_PAGE    = 'https://www.saucedemo.com/'
timeoutSmall = 10

# Hooks

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print(f'Step failed: {step}')
    print(f'Exception was: {exception}')
    # print(f'Scenario failed: {scenario}')
    # print(browser.get_screenshot_as_file("foo.png"))
    # browser.get_screenshot_as_file('screenshot.png')
    # util.fullpage_screenshot(self.driver, "test.png")


# Fixtures

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


# Shared Given Steps

@given('the website login page is displayed', target_fixture='login_page')
def login_page(browser):
    browser.maximize_window()
    browser.get(MAIN_PAGE)
    try:
        WebDriverWait(browser, timeoutSmall).until(
            EC.presence_of_element_located((By.ID, "login_button_container"))
        )
    except TimeoutException:
        raise Exception("Page is not loaded - Timeout")
    time.sleep(2)

@given('the products page is displayed', target_fixture='products_page')
def products_page(browser):
    login_page(browser)
    insert_my_text(browser, 'standard_user', 'user-name')
    insert_my_text(browser, 'secret_sauce', 'password')
    press_btn_by_id(browser, 'login-button')
    time.sleep(5)
    WebDriverWait(browser, timeoutSmall).until(EC.presence_of_element_located((By.ID, "inventory_container"))).is_displayed()
    headerTxt = browser.find_element(By.XPATH, "//*[@id='header_container']/div[2]/span").text
    assert headerTxt == "Products"


# Shared When Steps

@when(parsers.parse('press button by id "{name}"'))
def press_btn_by_id(browser, name):
    WebDriverWait(browser, timeoutSmall).until(EC.element_to_be_clickable((By.ID, name))).click()
    time.sleep(5)

@when(parsers.parse('the user inserts "{text}" to "{locator}"'))
def insert_my_text(browser, text, locator):
    time.sleep(1)
    if(text != "noValue"):
        WebDriverWait(browser, timeoutSmall).until(EC.presence_of_element_located((By.ID, locator))).send_keys(text)
    time.sleep(3)