""" Database access methods for AlbumServer http server. This program uses SQLite3.
    This is intended for educational use only. It is not very secure or robust. 
    
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
import os.path
import sqlite3
from sqlite3 import Error

class albumsDB:
    """database access methods for Albums database
    
       Parameters:
       mydb_file: path/name to sqlite3 database file
      
       TO DO:
       * Wrap database tranactions in try/catch blocks
       * Figure out how to display warnings/errors in browser
    """
    
    def __init__(self, mydb_file):
        self.db_file = mydb_file
        
        # make sure database file exists
        if not os.path.exists(self.db_file):
            sys.exit("Database file " + self.db_file + " not found. Program exiting.")
        
    def connect(self):
        """Create a database connection to the SQLite database
           specified by the db_file. Exit if connection fails.
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
        except Error as e:
            print(e)
            sys.exit("Unable to open database " + self.db_file + ". Program exiting.")
            
    def closeDB(self):
        self.cursor.close()
        self.conn.close()
        
    def get_albums(self):
        """Query all rows in the tasks table
           TO DO: handle empty table situation
        """
        
        self.cursor.execute("""
        select albumID, album_title, artist_name, year, label_name, price
        from Albums, Artists, RecordLabels
        where Albums.artistRef = Artists.artistID AND
        Albums.record_labelRef = RecordLabels.record_labelID
        order by album_title
        """)
        
        rows = self.cursor.fetchall()
        return rows
    
    def get_artists(self):
        self.cursor.execute("select artistID, artist_name, city, state from Artists order by artist_name") 
        
        rows = self.cursor.fetchall()
        return rows
    
    def get_tracks(self, albumID):
        """Get all tracks for a given albumID
        
           Params:
               albumID: ID of album to get tracks for
        """
        self.cursor.execute("""
        select tracknum, track_title, length
        from Tracks
        where Tracks.albumRef = ?
        order by tracknum
        """, (albumID,))
         
        rows = self.cursor.fetchall()
        return rows
    
    def get_labels(self):
        """Get all record labels"""
        
        self.cursor.execute("select record_labelID, label_name from RecordLabels order by label_name") 
        
        rows = self.cursor.fetchall()
        return rows
    
    def add_album(self, new_fields):
        """Insert a new album into albums table
        
           Params:
               new_fields: list of fields entered into new album form
        """
        # parse fields
        album_title = new_fields.get('album_title')[0]
        artistID = new_fields.get('artistID')[0]
        year = new_fields.get('year')[0]
        labelID = new_fields.get('labelID')[0]
        price = new_fields.get('price')[0]
        
        self.cursor.execute("""
        insert into Albums (price, album_title, artistRef, year, record_labelRef)
        values (?, ?, ?, ?, ?)""",
        (price, album_title, artistID, year, labelID))
        self.conn.commit()
        
    def add_track(self, new_fields):
        """Insert a single track into tracks table
        
           Params: new_fields: list of fields entered into new track form
        """
        # parse fields
        albumID = new_fields.get('albumID')[0]       # albumID is missing...
        track_num = new_fields.get('track_num')[0]
        track_title = new_fields.get('track_title')[0]
        track_length = new_fields.get('track_length')[0]
        
        print("add track: albumID: " + albumID + " title: " + track_title)
        
        self.cursor.execute("""
        insert into Tracks (albumRef, tracknum, track_title, length)
        values (?, ?, ?, ?)""",
        (albumID, track_num, track_title, track_length))
        self.conn.commit()
    
    def add_artist(self, new_fields):
        """Insert a new artist into artists table
        
           Params: 
               new_fields: list of fields entered into artist form
        """
        # parse fields
        artist_name = new_fields.get('artist_name')[0]
        city = new_fields.get('city')[0]
        state = new_fields.get('state')[0]
        
        # make sure artist does not exist in database already
        self.cursor.execute("select artistID from artists where artist_name = ?", ([artist_name]))
        artistID = self.cursor.fetchone()
        
        if artistID == None:
            # artist does not exist in database, so add artist to the table
            self.cursor.execute(
            'insert into Artists (artist_name, city, state) values (?, ?, ?)', (artist_name, city, state))
            self.conn.commit()
        else:
            print("Artist already exists in database")
            
    def add_label(self, new_fields):
        """Insert a new record label into record labels table
        
           Params: 
               new_fields: list of fields entered into record label form
        """
        # parse fields
        label_name = new_fields.get('label_name')[0]
        
        # make sure label does not exist in database
        self.cursor.execute("select record_labelID from RecordLabels where label_name = ?", ([label_name]))
        labelID = self.cursor.fetchone()
        
        if labelID == None:
            # label does not exist, so add it
            self.cursor.execute(
            'insert into RecordLabels (label_name) values (?)', ([label_name]))
            self.conn.commit()
        else:
            print("Label already exists in database")

