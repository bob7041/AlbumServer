# Album Server

Album Server is a simple Python Web Application. It is intended for use as an educational tool for learning Selenium programming. In other words, use it as a test target for Selenium practice. Several starter Python/Selenium scripts are included (more on that below), also intended as learning tools. Feel free to create your own Selenium scripts using your favorite programming language.

Album Server is a simple web-based Music Album database. Users can browse Albums and Artists, and add their own favorites to the database.

Album Server is easy to install and requires very little system resources to run, so it can be run on the same computer as the Selenium/Python scripts that are running against Album Server.

I had several goals in mind while developing this web app:

1. It had to be a non-trivial web application. Nothing too complicated but not too simplistic. Something that would provide an interesting application to test using Selenium.
   
2. It had to have a database back end so the database can be accessed via Python. However, the database had to be simple to create and re-create. This is a learning tool, so the database will be created and re-created over and over again. Album Server uses an SQLite database, and has a single python script that creates the database and fills it with data.
   
3. It had to have login capabilities to make it a little more realistic. It has a fake login page. Enter any user name, but the password must be "password"
   
4. It must be easy to install and not require a lot of configuration or dependencies. Album Server uses python and a little bit of CSS and Javascript.
   
5. It has to use very little system resources. I want to run Album Server on the same laptop that my Python/Selenium scripts will run on. Album  Server uses very little system resources.
   
This repository includes a few Python/Selenium scripts that target Album Server. These scripts are a good starting point for users learning Selenium programming:
   
   * SimpleTest1.py is a basic test that logs in, selects 2 albums, and verifies the correct price is displayed.
   * SelectRandomRow.py randomly selects an album and verifies the price. This shows how random number generators can be used to make tests more thorough (by not testing the same record every time).
   * AddArtists.py reads artists from a csv file and adds them to Album Server. This shows how to implement data driven testing in Python/Selenium. This script also verifies artists were successfully added by selecting the artists from the database, showing how Python can be used to work directly with a database.
     
Album Server is a pretty simple application, and is not very polished. There is very little error checking or styling. The emphasis was on getting a simple web application up and running. The polish will come later.

I also inserted several sleeps into the Selenium scripts to slow down processing so users can see the scripts in action.

## Installation

Installation is simple. The only prerequisite is Python (note that most Python distributions include SQLite. If yours does not, you will have to install it). Download  the code from github (eg clone this repository) and put it somewhere on your computer. 

To create the Album server database and fill it with test data, open a command prompt (Windows) or a terminal window (Linux) and cd to the AlbumServer\src directory. Then run the python script to create the database:

  python create_albumsdb.py
  
Note: this will create a new database complete with test data. If you ever want to erase the data and start over, simply re-run the script per the directions above. The script will prompt you to verify you want to delete the existing database. If you respond with y or Y the existing database will be deleted and a new one will be created, and test data loaded. The database is just a single file "albums.db" in the AlbumServer\database directory.

## Usage

Open a command prompt (Windows) or a terminal window (Linux) and cd to the AlbumServer\src directory. Start Album server with the following command:

  python web_server.py
  
Then point a browser to http://localhost:9000. The server can be stopped by typing control-C in the command prompt window.

To run any of the Python/Selenium scripts, open another command prompt/terminal window, cd to the AlbumServer\selenium directory, and enter the following command:

  python script_name
  
So for example to run the script "SimpleTest1.py" the command would be

  python SimpleTest1.py

## Contributions

I am not accepting Pull Requests at this time, but that will probably change in the future. If you are interested in contributing, please bear with me, I am still kinda new to github.

## License
GNU General Public License as published by the Free Software Foundation version 3
