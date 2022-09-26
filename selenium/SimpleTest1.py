""" PySeleniumTest1.py - a very basic python/selenium test script for testing
    Album Server web app. Log in, select a couple of albums, and
    verify the total price.
    
    Sleep statements inserted into key places so the user can see
    the test in action.
    
    This is not a production grade test, this is an educational
    tool for learning selenium.
    
    Fake Login page simulates logging in. User can enter any user name but password
    must be 'password'
    
    Copyright (C) July 2022  Bob Brander
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation version 3. The full license is 
    available here: https://opensource.org/licenses/GPL-3.0 
 
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# hit Album Server site
browser = webdriver.Firefox()
browser.get('http://localhost:9000/')

# log in
name = browser.find_element(By.ID, "loginName")
name.clear()
name.send_keys("bob")

pwd = browser.find_element(By.ID, "loginPassword")
pwd.clear()
pwd.send_keys("password")

time.sleep (2)

login_btn = browser.find_element(By.ID, "loginBtn")
login_btn.click()

# if invalid password entered, program hangs (maybe pop-up blocker?)
# maybe put login click in a try block

page_title = browser.title
if (page_title == "Albums"):
    print("Login Successfull")
else:
    browser.close ()
    sys.exit("Login failed. Test will terminate.")

# select 2 albums
album_table = browser.find_element(By.ID, "albums_table")
checkboxes = album_table.find_elements(By.ID, "buyme")
table_length = len(checkboxes)
if table_length < 2:
    browser.close ()
    sys.exit("Not enough data in table - test terminated.")

print("Table size: " + str(table_length))
    
checkboxes[0].click()
checkboxes[1].click()

# get the price for both checked rows
rows = album_table.find_elements(By.TAG_NAME, "tr")
cols = rows[1].find_elements(By.TAG_NAME, "td")
#cols[0].click()        # I don't know why but this does not work
price1 = cols[5].get_property("innerText")
print("Row 1 checked. Price: " + price1)

cols = rows[2].find_elements(By.TAG_NAME, "td")
price2 = cols[5].get_property("innerText")
print("Row 2 checked. Price: " + price2)

actual = float(price1) + float(price2)
expected = float(browser.find_element(By.ID, "total").get_attribute('value'))
if actual == expected:
    print("Test passed. Expected: " + str(expected) + " Actual: " + str(actual))
else:
    print("Test failed. Expected: " + str(expected) + " Actual: " + str(actual))
    
time.sleep (2)

# bye!
browser.close ()