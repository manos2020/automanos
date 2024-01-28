# Behavior-Driven Python with pytest-bdd #



# Python Installation and Tools #

Windows usage

Requires Python 3.
You can download the latest Python version from [Python.org](https://www.python.org/downloads/).


Usage of [Visual Studio Code](https://code.visualstudio.com/docs/languages/python).

Needed installallation of the appropriate browser and WebDriver executable.
These tests use Chromr and [chromedriver]



# Running Tests #

Running the test either with the runner of VSCode or with the following commands using allure reports as well:

Being in my assessment folder:

pytest --alluredir=.\allure-report .\tests\step_defs\test_authentication_als.py
pytest --alluredir=.\allure-report .\tests\step_defs\test_products_als.py

allure serve .\allure-report\ 

