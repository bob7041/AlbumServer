"""Database creation/load script for AlbumServer web app

    This program performs three tasks:
       
       1. Check to see if database file already exists. If it does,
          prompt user to verify deletion
       2. Create a new database file and create tables in database
       3. Load test data into database (from csv files located in datafiles 
          directory). Loading the data takes a few minutes - be patient.
       
    Notes: 
        * There is very little error checking here! 
        * csv data can be finicky. Apostrophies in input data in the csv files 
          may be displayed incorrectly. Replace apostrophies with single quotes.
          Commas in strings (eg "Emerson, Lake & Palmer") will cause the data to
          be broken up into separate fields. Remove commas in strings.
          Granted, this is not the best way to handle this, but this is an educational
          tool and not production ready software. 
    
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

import sys
import os
import csv
import sqlite3
from sqlite3 import Error

database_file = r"..\database\albums.db"

# 1. Check to see if database file exists, prompt user to confirm removal
  
if os.path.isfile(database_file):
    delete_database_file = input(database_file + " exists. Delete it (y/n)? ")
    if delete_database_file.upper() == 'Y':
        os.remove(database_file)
        print(database_file + " removed! Continuing with database creation.")
    else:
        # this line throws an exception for some reason, but still runs correctly
        sys.exit(database_file + " not removed. Exiting without further action." )
else:
    print(database_file + " not found. It will be created now.")

# 2. Create new database_file and create tables

print("Creating database and tables...")

dbconn = None
try:
    dbconn = sqlite3.connect(database_file)
    dbcursor = dbconn.cursor()
except Error as e:
    print(e)
    sys.exit("Unable to create new database file " + database_file + ". Program exiting.")

dbcursor.execute("""
CREATE TABLE Artists
(
	artistID integer primary key AUTOINCREMENT,
	artist_name text not null unique,
	city text,
    state text
);
""")

dbcursor.execute("""
CREATE TABLE RecordLabels
(
	record_labelID integer primary key AUTOINCREMENT,
	label_name text
);
""")

dbcursor.execute("""
CREATE TABLE Albums
(
    albumID integer primary key AUTOINCREMENT,
    price real,
	album_title text not null unique,
	artistRef integer not null,
	year integer not null,
	record_labelRef integer not null,
	FOREIGN KEY (artistRef) REFERENCES Artists (artistID),
	FOREIGN KEY (record_labelRef) REFERENCES RecordLabels (record_labelID)
);
""")

dbcursor.execute("""
CREATE TABLE Tracks
(
	trackID integer primary key AUTOINCREMENT,
	albumRef integer not null,
	tracknum integer not null,
	track_title text not null unique,
	length real,
	FOREIGN KEY (albumRef) REFERENCES Albums (albumID)
);
""")

dbconn.commit()

# 3. Load test data into new database

print("Loading test data into new database. This may take a few minutes...")

artists_file = r'..\datafiles\artists_initial_load.csv'

# make sure artists file exists and is readable
if not os.access(artists_file, os.R_OK):
            sys.exit("Input csv file " + artists_file + " not found. Program exiting.")
            
# load data from artists csv file into database
with open(artists_file) as artists_csv_file:
    artists_csv_reader = csv.reader(artists_csv_file, delimiter=',')
    line_count = 0
    for artist in artists_csv_reader:
        if line_count == 0:
            line_count += 1
        else:  
            dbcursor.execute('insert into Artists (artist_name, city, state) values (?, ?, ?)', (artist[0], artist[1], artist[2]))
            dbconn.commit()
            
            line_count += 1
    print("Inserted " + str(line_count-1) + " Aritsts")
artists_csv_file.close()

labels_file = r'..\datafiles\record_labels_initial_load.csv'

# make sure record labels file exists and is readable
if not os.access(labels_file, os.R_OK):
            sys.exit("Input csv file " + labels_file + " not found. Program exiting.")
            
# load data from labels csv file into database
with open(labels_file) as labels_csv_file:
    labels_csv_reader = csv.reader(labels_csv_file, delimiter=',')
    line_count = 0
    for label in labels_csv_reader:
        if line_count == 0:
            line_count += 1
        else:  
            dbcursor.execute('insert into RecordLabels (label_name) values (?)', (label[0],))
            dbconn.commit()
            
            line_count += 1
    print("Inserted " + str(line_count-1) + " Record Labels")
labels_csv_file.close()

albums_file = r'..\datafiles\albums_initial_load.csv'

# make sure albums file exists and is readable
if not os.access(albums_file, os.R_OK):
            sys.exit("Input csv file " + albums_file + " not found. Program exiting.")
            
# load data from albums csv file into database
with open(albums_file) as albums_csv_file:
    albums_csv_reader = csv.reader(albums_csv_file, delimiter=',')
    line_count = 0
    for album in albums_csv_reader:
        if line_count == 0:
            line_count += 1
        else:  
            dbcursor.execute('insert into Albums (price, album_title, artistRef, year, record_labelRef) values (?, ?, ?, ?, ?)', \
             (album[0], album[1], album[2], album[3], album[4]))
            dbconn.commit()
            
            line_count += 1
    print("Inserted " + str(line_count-1) + " Albums")
albums_csv_file.close()

tracks_file = r'..\datafiles\tracks_initial_load.csv'

# make sure tracks file exists and is readable
if not os.access(tracks_file, os.R_OK):
            sys.exit("Input csv file " + tracks_file + " not found. Program exiting.")
            
# load data from tracks csv file into database
with open(tracks_file) as tracks_csv_file:
    tracks_csv_reader = csv.reader(tracks_csv_file, delimiter=',')
    line_count = 0
    for track in tracks_csv_reader:
        if line_count == 0:
            line_count += 1
        else:  
            dbcursor.execute('insert into Tracks (albumRef, tracknum, track_title, length) values (?, ?, ?, ?)', \
             (track[0], track[1], track[2], track[3]))
            dbconn.commit()
            
            line_count += 1
    print("Inserted " + str(line_count-1) + " Tracks")
tracks_csv_file.close()

# tidy up

print("Process complete! New database created and test data loaded.")
dbcursor.close()
dbconn.close()
