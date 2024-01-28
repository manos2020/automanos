"""
This module contains step definitions for products_als.feature.
It uses Selenium WebDriver for browser interactions:
https://www.seleniumhq.org/projects/webdriver/
Setup and cleanup are handled using hooks.

"""

import time
from pytest_bdd import scenarios, when, then, parsers
from selenium.webdriver.common.by import By

# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

timeoutSmall = 10

# Scenarios

scenarios('../features/products_als.feature')


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
    WebDriverWait(browser, timeoutSmall).until(EC.element_to_be_clickable((By.ID, name))).click()
    time.sleep(5)

# Counts all the displayed products-items and presses the add to cart button for all individually
@when(parsers.parse('i add all the displayed product to cart'))
def add_displayed_products(browser):
    count = len(browser.find_elements(
        By.XPATH, "//div[contains(@class, 'inventory_list')]/div[contains(@class, 'inventory_item')]"))
    assert count > 0, 'No products available'
    for i in range(0,count):
        mynext = i + 1
        browser.find_element(
            By.XPATH,"//div[contains(@class, 'inventory_list')]/div["+str(mynext)+"]//button[contains(@class, 'btn_inventory')]").click()
        time.sleep(1)

# presses the add to cart button for the first displayed product, verifying in prior there is at least one
@when(parsers.parse('i add a product to cart'))
def add_a_product(browser):
    count = len(browser.find_elements(
        By.XPATH, "//div[contains(@class, 'inventory_list')]/div[contains(@class, 'inventory_item')]"))
    assert count > 0, 'No products available'
    browser.find_element(
        By.XPATH,"//div[contains(@class, 'inventory_list')]/div[1]//button[contains(@class, 'btn_inventory')]").click()
    time.sleep(1)

# presses the Remove to cart button for the first displayed product, verifying in prior there is at least one
@when(parsers.parse('i remove the product from cart'))
def remove_a_product(browser):
    count = len(browser.find_elements(
        By.XPATH, "//div[contains(@class, 'inventory_list')]/div[contains(@class, 'inventory_item')]"))
    assert count > 0, 'No products available'
    
    assert browser.find_element(
        By.XPATH,"//div[contains(@class, 'inventory_list')]/div[1]//button[contains(@class, 'btn_inventory')]").text == "Remove" , "Item you are trying to remove is not added correctly"
        

    browser.find_element(
        By.XPATH,"//div[contains(@class, 'inventory_list')]/div[1]//button[contains(@class, 'btn_inventory')]").click()
    time.sleep(1)

# Clicks on the Burger Menu and selects the relevant item according to the option used in the feature file
# Possible choices are only: Logout, Reset App State, About
@when(parsers.parse('i select "{myChoise}" from the burger Menu'))
def burger_menu(browser, myChoise):
    print(myChoise)
    browser.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(3)
    # locator with text contain Does not work correctly - and i used the else if statement
    # browser.find_element(By.XPATH, "//nav[contains(@class, 'bm-item-list')]/a[contains(text(),"+myChoise+")]").click()
    if(myChoise == "Logout"):
        browser.find_element(By.ID, "logout_sidebar_link").click()
    elif(myChoise == "Reset App State"):    
        browser.find_element(By.ID, "reset_sidebar_link").click()
    elif(myChoise == "About"):    
        browser.find_element(By.ID, "about_sidebar_link").click()
    else:
        raise Exception("Not correct choice user for the burger menu")
    time.sleep(5)

# From the sorting dropdown in products page, selects the item requested e.g lohi
@when(parsers.parse('select from sorting dropdown the "{text}"'))
def select_from_dropdown_with_name(browser, text):
    dropdown = Select(WebDriverWait(browser, timeoutSmall).until(
        EC.presence_of_element_located((By.XPATH, "//select[contains(@class, 'product_sort_container')]"))))
    dropdown.select_by_value(text)
    time.sleep(5)


# # Then Steps

# Checking if the products page is loaded, or in error case check if error message appears and verify that matches
@then(parsers.parse('wait for products page to be loaded "{errorCase}" or "{myMsg}"'))
def products_page_manipulation(browser, errorCase, myMsg):
    # if(errCase != "0"):
    if(errorCase):
        time.sleep(5)
        browser.find_element(By.XPATH, "//div[contains(@class, 'error-message-container')]")
        WebDriverWait(browser, timeoutSmall).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'error-message-container')]"))).is_displayed()
        errorTxt = browser.find_element(By.XPATH, "//div[contains(@class, 'error-message-container')]/h3").text
        assert errorTxt == myMsg
    else:
        # Trying to verify a correct load of the page of products and checks in parallel the header text to be Products
        WebDriverWait(browser, timeoutSmall).until(
            EC.presence_of_element_located((By.ID, "inventory_container"))).is_displayed()
        headerTxt = browser.find_element(By.XPATH, "//*[@id='header_container']/div[2]/span").text
        assert headerTxt == "Products"

# Verifies that the product count should be the given one
@then(parsers.parse('the products count should be "{expectedNo}"'))
def products_count(browser, expectedNo):
    elements = browser.find_elements(
        By.XPATH, "//div[contains(@class, 'inventory_list')]/div[contains(@class, 'inventory_item')]")
    # count = len(elements)
    assert len(elements) == int(expectedNo)

# Goes through all the products displayed and checks the title links to be clickable and the add to cart to be clickable
@then(parsers.parse('all specific product links should be clickable'))
def products_count_and_clickability(browser):
    count = len(browser.find_elements(
        By.XPATH, "//div[contains(@class, 'inventory_list')]/div[contains(@class, 'inventory_item')]"))
    assert count > 0, 'No products available'
    for i in range(0,count):
        browser.find_element(By.ID, "item_"+str(i)+"_title_link").is_displayed()
        WebDriverWait(browser, timeoutSmall).until(
            EC.element_to_be_clickable((By.ID, "item_"+str(i)+"_title_link")))
        mynext = i + 1
        WebDriverWait(browser, timeoutSmall).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'inventory_list')]/div["+str(mynext)+"]//button[contains(@class, 'btn_inventory')]")))

# For all displayed products, verifies that the button text is Add to cart        
@then(parsers.parse('all displayed products are available for adding to cart'))
def products_availability(browser):
    count = len(browser.find_elements(
        By.XPATH, "//div[contains(@class, 'inventory_list')]/div[contains(@class, 'inventory_item')]"))
    assert count > 0, 'No products available'
    for i in range(0,count):
        mynext = i + 1
        assert browser.find_element(
                 By.XPATH,"//div[contains(@class, 'inventory_list')]/div["+str(mynext)+"]//button[contains(@class, 'btn_inventory')]").text == "Add to cart" , "Button for adding to cart is not in the correct state"

# Verifies the shopping cart badge to be the expected
@then(parsers.parse('i verify the shopping cart badge to have the correct number'))
def verif_cart_number(browser):
    assert browser.find_element(
                 By.XPATH,"//span[contains(@class, 'shopping_cart_badge')]").text == "6" , "Incorrect cart badge number appears"

# Verifies the shopping cart badge to be the expected
@then(parsers.parse('i verify the shopping cart badge to be "{expectedNo}"'))
def verif_cart_number(browser, expectedNo):
    if(int(expectedNo)):
        assert browser.find_element(
                 By.XPATH, "//span[contains(@class, 'shopping_cart_badge')]").text == expectedNo , "Incorrect cart badge number appears"
    else:
        WebDriverWait(browser, timeoutSmall).until(
            EC.invisibility_of_element_located((By.XPATH, "//span[contains(@class, 'shopping_cart_badge')]")))

# Checks the authentication page to be loaded
@then(parsers.parse('authentication page is loaded'))
def logout_happened(browser):
    try:
        WebDriverWait(browser, timeoutSmall).until(
            EC.presence_of_element_located((By.ID, "login_button_container"))
        )
    except TimeoutException:
        raise Exception("logout did not work correctly - irrelevant page was displayed")

# Checks the general home page to be loaded
@then(parsers.parse('genaral home page is loaded'))
def about_happened(browser):
    try:
        WebDriverWait(browser, timeoutSmall).until(
            EC.presence_of_element_located((By.ID, "__next"))
        )
    except TimeoutException:
        raise Exception("about did not work correctly - irrelevant page was displayed")

# Clicks on the shopping cart btn
@when(parsers.parse('click on the shopping cart'))
def shopping_cart(browser):
    WebDriverWait(browser, timeoutSmall).until(
        EC.element_to_be_clickable((By.ID, "shopping_cart_container"))).click()
    time.sleep(5)

# Checks the cart contents page to be loaded
@then(parsers.parse('the cart contents should be loaded'))
def verif_cart_loaded(browser):
    time.sleep(2)
    WebDriverWait(browser, timeoutSmall).until(
        EC.presence_of_element_located((By.ID, "cart_contents_container"))).is_displayed()

# Checks the "{myChoise}" page to be loaded - myChoise can be info, summary, complete
@then(parsers.parse('the checkout "{myChoise}" page should be loaded'))
def verif_checkout_info_loaded(browser, myChoise):
    time.sleep(2)
    WebDriverWait(browser, timeoutSmall).until(
        EC.presence_of_element_located((By.ID, "checkout_"+myChoise+"_container"))).is_displayed()

# The below code intentionally left commented for purposes of the assignment
    
# @then(parsers.parse('the checkout info page should be loaded'))
# def verif_checkout_info_loaded(browser):
#     time.sleep(2)
#     WebDriverWait(browser, timeoutSmall).until(EC.presence_of_element_located((By.ID, "checkout_info_container"))).is_displayed()

# @then(parsers.parse('the checkout overview page should be loaded'))
# def verif_checkout_overview_loaded(browser):
#     time.sleep(2)
#     WebDriverWait(browser, timeoutSmall).until(EC.presence_of_element_located((By.ID, "checkout_summary_container"))).is_displayed()

# @then(parsers.parse('the checkout complete page should be loaded'))
# def verif_checkout_overview_loaded(browser):
#     time.sleep(2)
#     WebDriverWait(browser, timeoutSmall).until(EC.presence_of_element_located((By.ID, "checkout_complete_container"))).is_displayed()

# Verifies that the sorting of products with lohi price has been done correctly
@then(parsers.parse('i verify the the sort by price low to high has happened'))
def lohi_sorting_verif(browser):
    count = len(browser.find_elements(
        By.XPATH, "//div[contains(@class, 'inventory_list')]/div[contains(@class, 'inventory_item')]"))
    assert count > 0, 'No products available'
    myList = []
    for i in range(0,count):
        mynext = i + 1
        myList.append(browser.find_element(
            By.XPATH,"//div[contains(@class, 'inventory_list')]/div["+str(mynext)+"]//div[contains(@class, 'inventory_item_price')]").text)
        time.sleep(1)
    capturedList = myList
    myList.sort()
    assert capturedList == myList