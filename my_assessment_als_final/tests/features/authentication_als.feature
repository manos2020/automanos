@web @auth
Feature: Test case 001
  As a Product owner,
  I want to check the authentication of the xxx site using different user categories,
  So that the user management to be used correctly in the relevant eshop

  Background:
    Given the website login page is displayed

# Due to the simplicity of the locators, i am abusing the usage of the locators here (for now)
  Scenario Outline: Authentication and user management
    When the user inserts "<username>" to "user-name"
    And the user inserts "<password>" to "password"
    And press button by id "login-button"
    Then wait for products page to be loaded "<errorCase>" or "<myMsg>"

    Examples: Combinations
      | username         | password      | errorCase | myMsg                                                                     |
      | standard_user    | secret_sauce  | 0         | noValue                                                                   |
      | standard_user    | noValue       | 1         | Epic sadface: Password is required                                        |
      | noValue          | secret_sauce  | 1         | Epic sadface: Username is required                                        |
      | locked_out_user  | secret_sauce  | 1         | Epic sadface: Sorry, this user has been locked out.                       |
      | myRandom         | myRandom      | 1         | Epic sadface: Username and password do not match any user in this service |
