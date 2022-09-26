""" AddArtists - a simple data-driven Python/Selenium scipt to read 
    data from a csv file (list of artists in this case) and insert 
    the data into the Album Server database (Artists table).
    
    NOTE: if you run this script, you must manually delete the inserted
    records from the database table Artists before running this script 
    again. If you don't delete the records from the database, you will 
    get errors when you run this script again (because the data you are 
    trying to insert is already in the database and can't be duplicated).
    Alternatively you can replace the artists in csv file with new artists.
    
    This is not a production-ready program. It is meant as an 
    educational tool to show what can be done with Python and Selenium.
    
    Copyright (C) August 2022  Bob Brander
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation version 3. The full license is 
    available here: https://opensource.org/licenses/GPL-3.0 
 
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
"""

import os
import csv 
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3
from sqlite3 import Error

artists_file = r'..\datafiles\Artists.csv'
  
# make sure input file exists and is readable
if not os.access(artists_file, os.R_OK):
            sys.exit("Input csv file " + artists_file + " not found. Program exiting.")
  
# connect to the database
db_connection = None
try:
    db_connection = sqlite3.connect(r"..\database\albums.db")
    print("Conected to sqlite database")
except Error as e:
    print(e)
    sys.exit("Unable to connect to database. Test terminated")
cursor = db_connection.cursor()
    
# hit the Album Server app
browser = webdriver.Firefox()                 # utf-8 encoding crashes here!
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

# verify successfull login
page_title = browser.title
if (page_title == "Albums"):
    print("Login Successfull")
else:
    browser.close ()
    sys.exit("Login failed. Test terminated.")
    
# read csv file and add each row to artists table 
with open(artists_file) as artists_csv_file:
    artists_csv_reader = csv.reader(artists_csv_file, delimiter=',')
    
    for artist in artists_csv_reader:
        print(artist[0] + '|' + artist[1] + '|' + artist[2])

        # navigate to Add Artists page
        add_artists_link = browser.find_element(By.LINK_TEXT, "Add Artist")
        add_artists_link.click()

        # verify we are on add artists page
        page_title = browser.title
        if (page_title == "Add an Artist"):
            print("Navigated to Add Artist page")
        else:
            browser.close ()
            sys.exit("Unable to find Add Artist page. Test terminated.")

        artist_name = browser.find_element(By.ID, "aname")
        artist_name.send_keys(artist[0])
    
        artist_city = browser.find_element(By.ID, "acity")
        artist_city.send_keys(artist[1])
    
        artist_state = browser.find_element(By.ID, "astate")
        artist_state.send_keys(artist[2])
        
        add_button = browser.find_element(By.ID, "add_artist")
        add_button.click()
    
        # verify artists were added to database
        cursor.execute("""
        select artistID
        from Artists
        where artist_name = ? AND
        city = ? AND
        state = ?""", (artist[0], artist[1], artist[2]))
        
        artist_search = cursor.fetchone()
        if artist_search[0] > 0:
            print(artist[0] + " successfully added to database!")   
            
        time.sleep(2)            
        
# bye!
artists_csv_file.close()
db_connection.close()
browser.close ()