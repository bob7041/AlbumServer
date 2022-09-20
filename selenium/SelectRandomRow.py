""" PySeleniumTest2.py - a very basic pytohn/selenium test script for testing
    Album Server web app. Randomly select an album from the list and
    verify the price. This is a very simplistic example of making 
    a test script that does not test the same thing every time.
    
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
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# hit Album Server site
browser = webdriver.Firefox()
browser.get('http://localhost:9000/')

# log in
name = browser.find_element_by_id("loginName")
name.clear()
name.send_keys("bob")

pwd = browser.find_element_by_id("loginPassword")
pwd.clear()
pwd.send_keys("password")

time.sleep (2)

login_btn = browser.find_element_by_id("loginBtn")
login_btn.click()

# if invalid password entered, program hangs (maybe pop-up blocker?)
# maybe put login click in a try block

page_title = browser.title
if (page_title == "Albums"):
    print("Login Successfull")
else:
    browser.close ()
    sys.exit("Login failed. Test will terminate.")

# get number of rows in table
album_table = browser.find_element_by_id("albums_table")
checkboxes = album_table.find_elements_by_id("buyme")
table_length = len(checkboxes)
if table_length < 2:
    browser.close ()
    sys.exit("Not enough data in table - test terminated.")

print("Table size: " + str(table_length))
 
# randomly select an album
r = random.randrange(0, table_length-1)
checkboxes[r].click()

# get the price for checked row
# rows starts at table header, so add offset of +1
rows = album_table.find_elements_by_tag_name("tr")
cols = rows[r+1].find_elements_by_tag_name("td")
#cols[0].click()        # I don't know why but this does not work
price = cols[5].get_property("innerText")
print("Row " + str(r+1) + " checked. Price: " + str(price))

actual = float(price) 
expected = float(browser.find_element_by_id("total").get_attribute('value'))
if actual == expected:
    print("Test passed. Expected: " + str(expected) + " Actual: " + str(actual))
else:
    print("Test failed. Expected: " + str(expected) + " Actual: " + str(actual))
    
time.sleep (2)

# bye!
browser.close ()