## Welcome
Hello, this is my CS50 capstone project Blackjack.
## Link
Here is a link to a demonstration of this project
https://www.youtube.com/watch?v=ohPHhQ6x0so
## Environments used
This project uses Flask, Jinja2, HTML, CSS, SQL, and python. Therefore you will need to have all of these environments downloaded.
I recommend using homebrew to install these environments. Homebrew can be found on the web. However, if you are in CS50's
VSCode environment, then there is no need to install any of these.
## How to install
Now once you have downloaded the zipfile, to run/test the application, you will need to follow these instructions typing
the respective commands in your github terminal
execute
```bash
unzip blackjack.zip
```
execute
```bash
rm blackjack.zip
```
respond with
```bash
y
```
```bash
cd blackjack
```
now you can run the program with the following command
```bash
flask run
```
now a developmental server will be running and you can use such server to use the website.
Make sure to not input any real passwords!
## Folders within the app
Now within this file you will find the following folders: flask_session, static, templates.
Within flask_session, you will see the session that the page runs on.
Within static, you all the CSS files used to style the website along with all the images used in the website.
Within templates you will find all the html pages that are used within the website
## Files within the app
Now besides these folders, you will see the following files: app.py, blackjack.db, DESIGN.md, game.py, helpers.py, README.md
The last one, README.md is the one you are currently in providing instructions on how to use my applicaiton.
The other markdown file is DESIGN.md which discusses how I implemented my project technically and explains my design decisions.
Now within app.py, you will find all of the code needed to make the actual website functional
Within helpers.py, you will find helper functions used within the app.py file to assist with rendering the apology screen
and with the account registration, login, and resetpassword functions.
Within game.py, you will find all the functions used to make the game object work in the app.py function. For understanding how
I made a Blackjack emulator, I would recommend paying the closest attention to this file as it is where all the magic happens.
You can actually modify that file by adding print commands and a function to get user input to make a blackjack game playable via
the command lines on your terminal. Besides that this function contains the game class which has all the functions and variables
needed to make this game work on the backend of the server. The last file yet to be discussed is blackjack.db which is the database which
stores all data for the users on the app and for the all the games played.
## Last things
Last things before I let you explore this application.

I hope that you enjoy using this project, I hope this readme explains everything necessary.
Anyone is welcome to use anything in this project. No references needed!
If any problems/questions arise , feel free to email me at: andrewleblanc@college.harvard.edu

