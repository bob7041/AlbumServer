""" AlbumServer - a very basic (and not very secure or robust) http app server intended  
    for educational use only. This server implements a basic web-based artist/album 
    database using an SQLite3 database. This server is intended for use in learning 
    python/selenium programming. This server is based on the basic server here:
    https://www.pythonpool.com/python-http-server/
    
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
    
    TO DO:
        * Add search/next/prev and add/edit/delete capabilities to forms 
        * Add some styling (especially buttons at top of pages)
        * Add an Order form?
        * Use match/case in place of the large if/elif constructs in do_GET and
          do_POST below?
        * How to store time in the database? It seems to take both "3.5" and 
          "3:50" formats (which are both correct but can cause problems if we 
          want to do any calculations with track times)
        * In albums.html, change Add2Total so it adds/subtracts only the row that
          was just checked/unchecked. It currently uses a brute-force method
          that loops thru all records and adds up the total for all checked rows
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import re
import albumsdb

# hardcoded global parameters
hostname = "localhost"
serverport = 9000
database_file = r"..\database\albums.db"
 
# dynamically build list of links to add to each html page. This can be
# done easily by using "replace {{links}}" in each method that builds
# an html page from a template. Is there a better place to put this list?
# Can't put in MyServer because MyServer is never instantiated.
base = hostname + ":" + str(serverport) + "/"  
links = ("<a href=http://" + base + "albums>Albums</a>\n"
         "<a href=http://" + base + "artists>Artists</a>\n" 
         "<a href=http://" + base + "labels>Labels</a>\n" +
         "<a href=http://" + base + "add_album>Add Album</a>\n" +
         "<a href=http://" + base + "add_track>Add Track</a>\n" +
         "<a href=http://" + base + "add_artist>Add Artist</a>\n" +
         "<a href=http://" + base + "add_label>Add Label</a>\n" +
         "<a href=http://" + base + ">Logout</a>")
        
class MyServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """determine where to go when user clicks a link"""
        
        # replace if/elif with match/case?
        if (self.path == "/"):   
            self.display_unmodified_form(r"..\html\fake_login.html")
        elif ("/albums" in self.path):
            self.get_albums()
        elif ("/artists" in self.path):
            self.get_artists()
        elif ("/labels" in self.path):
            self.get_labels()
        elif ("/tracks" in self.path):
            # albumID is after the ? in path eg "tracks?ID=4"
            match = re.search('\d+$', self.path)
            albumID = match.group()
            self.get_tracks(albumID)
        elif ("/add_album" in self.path):
            self.put_album_form()
        elif ("/add_artist" in self.path):
            self.display_unmodified_form(r"..\html\add_artist_form.html")
        elif ("/add_track" in self.path):
            self.put_track_form()
        elif ("/add_label" in self.path):
            self.display_unmodified_form(r"..\html\add_label_form.html")
    
    def do_POST(self):
        """determine what to do when user clicks a submit button on a form"""
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
        
        if self.path == '/add_album':
            my_albumsdb.add_album(fields)
            self.get_albums()
        elif self.path == '/add_track':
            my_albumsdb.add_track(fields)
            self.put_track_form()
        elif self.path == '/add_artist':
            my_albumsdb.add_artist(fields)
            self.get_artists()
        elif self.path == '/add_label':
            my_albumsdb.add_label(fields)
            self.get_labels()
        
    def get_albums(self):
        """retrieve a list of albums from database and display the list"""
        # get template
        try:
            with open(r"..\html\albums.html") as f:
                file = f.read()
        except Exception as e:
            print(e)
            self.send_response(500, "Failed")
            self.end_headers()
            self.wfile.write(bytes(e, "utf-8"))
            return
        
        # format album data from database
        table_data = my_albumsdb.get_albums()
        table_row = ""
        baseURL = "http://" + hostname + ":" + str(serverport)
        for data in table_data:
            albumID = str(data[0])
            album_title = data[1]
            artist_name = data[2]
            year = str(data[3])
            label_name = data[4]
            price = str(data[5])
            
            table_row += "<tr><td><input type='checkbox' onclick='Add2Total()' id='buyme'></td>"
            
            # embed albumID in URL so tracks know which album 
            table_row += ("<td><a href=" + baseURL + "/tracks?ID=" + albumID + ">" + album_title + "</a></td>" +
                         "<td>" + artist_name + "</td><td>" + year + "</td>" +
                         "<td>" + label_name + "</td><td>" + price + "</td></tr>")
    
        # add links to top of page
        file = file.replace("{{links}}", links)
        # replace {{db_records}} in template by table_row
        file = file.replace("{{db_records}}", table_row)
        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(bytes(file, "utf-8"))
        
    def get_artists(self):
        """retrieve list of artists from database and display the list"""
        # get template
        try:
            with open(r"..\html\artists.html") as f:
                file = f.read()
        except Exception as e:
            print(e)
            self.send_response(500, "Failed")
            self.end_headers()
            self.wfile.write(bytes(e, "utf-8"))
            return
        
        # format artist data from database
        table_data = my_albumsdb.get_artists()
        table_row = ""
        for data in table_data:
            # row should look like: artist | origin
            # skip data[0] as this is the artistID
            table_row += "<tr><td>" + data[1] + "</td><td>" + data[2] + "</td><td>" + data[3] + "</td></tr>"
       
        # add links to top of page
        file = file.replace("{{links}}", links)
        # replace {{db_records}} in template by table_row
        file = file.replace("{{db_records}}", table_row)
        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(bytes(file, "utf-8"))
    
    def get_labels(self):
        """retrieve list of record labels from database and display the list"""
        # get template
        try:
            with open(r"..\html\labels.html") as f:
                file = f.read()
        except Exception as e:
            print(e)
            self.send_response(500, "Failed")
            self.end_headers()
            self.wfile.write(bytes(e, "utf-8"))
            return
        
        # format record labels data from database
        table_data = my_albumsdb.get_labels()
        table_row = ""
        for data in table_data:
            # skip data[0] as this is the record_lableID
            table_row += "<tr><td>" + data[1] + "</td></tr>"
            
        # add links to top of page
        file = file.replace("{{links}}", links)
        # replace {{db_records}} in template by table_row
        file = file.replace("{{db_records}}", table_row)
        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(bytes(file, "utf-8"))
        
    def get_tracks(self, albumID):
        """retrieve list of album tracks for selected album from database and
           display the list
        
           Parameters: albumID: ID of selected album
        """
        # get template
        try:
            with open(r"..\html\tracks.html") as f:
                file = f.read()
        except Exception as e:
            print(e)
            self.send_response(500, "Failed")
            self.end_headers()
            self.wfile.write(bytes(e, "utf-8"))
            return
        
        # format track data from database
        table_data = my_albumsdb.get_tracks(albumID)
        table_row = ""
        for data in table_data:
            # data[0] is an int so convert it to string
            sequence = str(data[0])
            table_row += "<tr><td>" + sequence + "</td><td>" + data[1] + "</td><td>" + str(data[2]) + "</td></tr>"
        
        # add links to top of page (but tracks page only gets 2 links)
        track_links = ("<a href=http://" + base + "albums>Back</a>\n"
                       "<a href=http://" + base + ">Logout</a>\n") 
        file = file.replace("{{links}}", track_links)
        
        # replace {{db_records}} in template by table_row
        file = file.replace("{{db_records}}", table_row)
        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(bytes(file, "utf-8"))
    
    def put_album_form(self):
        """display the new album form"""
        try:
            with open(r"..\html\add_album_form.html") as f:
                file = f.read()
        except Exception as e:
            print(e)
            self.send_response(500, "Failed")
            self.end_headers()
            self.wfile.write(bytes(e, "utf-8"))
            return
        
        # build menu list of all valid artists in database
        # artist menu options need to  look like this: <option value="1">Santana</option>
        artist_menu_data = my_albumsdb.get_artists()
        artist_options = ""
        for artist_data in artist_menu_data:
            artist_options += "<option value=" + str(artist_data[0]) + ">" + artist_data[1] + "</option>"
            
        # build menu list of all valid record labels in database
        # record label menu options need to look like:  <option value="CBS Records">CBS Records</option>
        label_menu_data = my_albumsdb.get_labels()
        label_options = ""
        for label_data in label_menu_data:
            label_options += "<option value=" + str(label_data[0]) + ">" + label_data[1] + "</option>"
            
        # add links to top of page
        file = file.replace("{{links}}", links)
        # replace {{artist_records}} in template by artist_options
        file = file.replace("{{artist_records}}", artist_options)
        # replace {{record_labels }} in template by label_options
        file = file.replace("{{record_labels}}", label_options)
        
        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(bytes(file, "utf-8"))

    def put_track_form(self):
        """add a track for selected album"""
        # get template
        try:
            with open(r"..\html\add_track_form.html") as f:
                file = f.read()
        except Exception as e:
            print(e)
            self.send_response(500, "Failed")
            self.end_headers()
            self.wfile.write(bytes(e, "utf-8"))
            return
        
        # build menu list of all valid albums in database
        # menu options should look like "albumID | album title"
        album_menu_data = my_albumsdb.get_albums()
        album_options = ""
        for album_data in album_menu_data:
            album_options += "<option value=" + str(album_data[0]) + ">" + album_data[1] + "</option>"
            
        # add links to top of page
        file = file.replace("{{links}}", links)
        # replace {{artist_records}} in template by artist_options
        file = file.replace("{{album_records}}", album_options)
               
        # replace {{db_records}} in template by album_options
        #file = file.replace("{{db_records}}", album_options)
        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(bytes(file, "utf-8"))
    
    def display_unmodified_form(self, display_me):
        """display a form that does not need any modifications"""
        try:
            with open(display_me) as f:
                file = f.read()
        except Exception as e:
            print(e)
            self.send_response(500, "Failed")
            self.end_headers()
            self.wfile.write(bytes(e, "utf-8"))
            return
        
        # add links to top of page
        file = file.replace("{{links}}", links)
        
        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(bytes(file, "utf-8"))
        
if __name__ == "__main__":   
    # connect to database
    my_albumsdb = albumsdb.albumsDB(database_file)
    my_albumsdb.connect()
    
    webServer = HTTPServer((hostname, serverport), MyServer)
    print(f"Server started http://{hostname}:{serverport}")
 
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
 
    my_albumsdb.closeDB()
    webServer.server_close()
    print("Http server stopped.")