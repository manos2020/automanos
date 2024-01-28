@web @products
Feature: Test case 002
  As a Product owner,
  I want to verify the products page and add/remove to cart functionality
  So that the links are available and products ready to add to cart - proper add/remove functional
  This feature will include more features for simplicity reason - part of the assessment

  Background:
    Given the products page is displayed

  Scenario: The products page appearance
    Then the products count should be "6"
    And all specific product links should be clickable
    And all displayed products are available for adding to cart

  Scenario: Adding my displayed products to cart
    When i add all the displayed product to cart
    Then i verify the shopping cart badge to have the correct number

  Scenario: Adding and removing products to cart
    When i add a product to cart
    Then i verify the shopping cart badge to be "1"
    When i remove the product from cart
    # Actually Checking the invisibility here 
    Then i verify the shopping cart badge to be "0"

Scenario: Burger Menu logout
    When i select "Logout" from the burger Menu
    Then authentication page is loaded

Scenario: Burger Menu about
    When i select "About" from the burger Menu
    Then genaral home page is loaded

Scenario: Burger Menu reset app
    When i add all the displayed product to cart
    When i select "Reset App State" from the burger Menu
    Then i verify the shopping cart badge to be "0"
    And all displayed products are available for adding to cart


# for simplicity reasons and as part of an assignment - just checking the sunny day scenario
Scenario: Check out
    When i add a product to cart
    And click on the shopping cart
    Then the cart contents should be loaded
    When press button by id "checkout"
    Then the checkout "info" page should be loaded
    When the user inserts "thisIsMyName" to "first-name"
    And the user inserts "thisIsMySurname" to "last-name"
    And the user inserts "12345" to "postal-code"
    And press button by id "continue"
    Then the checkout "summary" page should be loaded
    When press button by id "finish"
    Then the checkout "complete" page should be loaded

Scenario: Sort items by price low to high
    When select from sorting dropdown the "lohi"
    Then i verify the the sort by price low to high has happened