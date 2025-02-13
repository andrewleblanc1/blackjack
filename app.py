# backend adapted from CS50's Finance
import random
import os
import sqlite3
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from game import game

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure to use SQLite database
db = sqlite3("sqlite:///blackjack.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# placeholders for to store a game object and wager value globally
games = {}
wagers = {}


@app.route("/game", methods=["GET", "POST"])
@login_required
def gameO():
    user_id = session["user_id"]
    if request.method == "GET":
        return redirect("/")
    if request.method == "POST":
        # ensure user provides an input in playgame.html
        moneydict = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        if not request.form.get("wager"):
            return apology("Must provide a wager", 400)
        # ensure user inputs a valid wager amount
        money = moneydict[0]["cash"]
        if money < int(request.form.get("wager")):
            return apology("you do not have enough money", 400)
        # makes sure user has enough money
        wager = request.form.get("wager")
        try:
            int(wager)
        except ValueError:
            return apology("Must provide positive integer")
        wager = int(wager)
        if wager < 1:
            return apology("Must provide positive integer")
        wagers[user_id] = wager
        if wagers == None:
            return redirect("/playgame")
        # starts and stores game globally
        newgame = game()
        newgame.startGame()
        games[user_id] = newgame
        coverDealerimg = [newgame.dealerimg[0], "cover"]
        newgame.checkblackjack()
        # If blackjack, ends game and adds result to the game database while also updating the users cash amount in the database ( adding double the
        # wager amount to their cash holdings)
        if newgame.blackjack:
            newgame.getResult()
            profit = wagers[user_id] * 2
            db.execute("INSERT INTO game(result, money, userid) VALUES (?,?,?)",
                       newgame.result, profit, user_id)
            originalCashdict = db.execute("select cash from users where id = ?", user_id)
            originalCash = originalCashdict[0]['cash']
            newamount = originalCash + profit
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newamount, user_id)
            return render_template("result.html", playerimg=newgame.playerimg, dealerimg=coverDealerimg, result=newgame.result)
        return render_template("game.html", playerimg=newgame.playerimg, dealerimg=coverDealerimg)


@app.route("/hit", methods=["GET", "POST"])
@login_required
def hit():
    # gets user id to access game and wage in the global dictionary
    user_id = session["user_id"]
    newgame = games.get(user_id)
    # protects against users accessing the page by typing into their browser
    if newgame == None:
        return redirect("/")
    if request.method == "GET":
        return redirect("/")
    if request.method == "POST":
        # adds card to player hand and checks if value is over 21, if so player loses and the result of the game is added into the database
        # while also subtracting wager from their cash amount in the database and rendering the result template, if their value is 21, goes to a runoff
        # (runoff descrbed in game.py)
        # if it is less than 21, renders page again with new hand
        coverDealerimg = [newgame.dealerimg[0], "cover"]
        newgame.addPlayerCard()
        newgame.calculatePlayerValue()
        if newgame.playerValue == 21:
            return redirect("/result")
        if newgame.checkbust():
            newgame.getResult()
            loss = wagers[user_id] * -1
            db.execute("INSERT INTO game(result, money, userid) VALUES (?,?,?)",
                       newgame.result, loss, user_id)
            originalCashdict = db.execute("select cash from users where id = ?", user_id)
            originalCash = originalCashdict[0]['cash']
            newamount = originalCash + loss
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newamount, user_id)
            return render_template("result.html", playerimg=newgame.playerimg, dealerimg=coverDealerimg, result=newgame.result)
        return render_template("game.html", playerimg=newgame.playerimg, dealerimg=coverDealerimg)


@app.route("/result", methods=["GET", "POST"])
@login_required
def resultOfGame():
    # gets user id to access game and wage in the global dictionary
    user_id = session["user_id"]
    newgame = games.get(user_id)
    # protects against users accessing the page by typing into their browser
    if request.method == "GET":
        if newgame == None:
            return redirect("/")
        coverDealerimg = [newgame.dealerimg[0], "cover"]
        # checks for blackjack, renders result accordingly if blackjack
        if newgame.blackjack:
            result = newgame.result
            return render_template("result.html", playerimg=newgame.playerimg, dealerimg=coverDealerimg, result=result)
        # if value is 21, goes to a runoff, and renders result template according to whether there is a house win, player win, or push
        # For all results, game will be added to the games database. If house wins, players cash holding in the database will be subtracted by the
        # wager amount, If player wins, players cash holding in the database will be added by the wager amount. The result template will
        # be rendered according to the result and shows both the user and dealer hands.
        if newgame.playerValue == 21:
            newgame.runoff()
            newgame.getResult()
            result = newgame.result
            if result == "House Wins!":
                loss = wagers[user_id] * -1
                db.execute("INSERT INTO game(result, money, userid) VALUES (?,?,?)",
                           newgame.result, loss, user_id)
                originalCashdict = db.execute("select cash from users where id = ?", user_id)
                originalCash = originalCashdict[0]['cash']
                newamount = originalCash + loss
                db.execute("UPDATE users SET cash = ? WHERE id = ?", newamount, user_id)
            if result == "Player Wins!":
                profit = int(wagers[user_id])
                db.execute("INSERT INTO game(result, money, userid) VALUES (?,?,?)",
                           newgame.result, profit, user_id)
                originalCashdict = db.execute("select cash from users where id = ?", user_id)
                originalCash = originalCashdict[0]['cash']
                newamount = originalCash + profit
                db.execute("UPDATE users SET cash = ? WHERE id = ?", newamount, user_id)
            if result == "Push":
                profit = 0
                db.execute("INSERT INTO game(result, money, userid) VALUES (?,?,?)",
                           newgame.result, profit, user_id)
            return render_template("result.html", playerimg=newgame.playerimg, dealerimg=newgame.dealerimg, result=result)
        return redirect("/")
    if request.method == "POST":
        # Game goes to a runoff, and renders result template according to whether there is a house win, player win, or push
        # For all results, game will be added to the games database. If house wins, players cash holding in the database will be subtracted by the
        # wager amount, If player wins, players cash holding in the database will be added by the wager amount. The result template will
        # be rendered according to the result and shows both the user and dealer hands.
        newgame.runoff()
        newgame.getResult()
        result = newgame.result
        if result == "House Wins!":
            loss = wagers[user_id] * -1
            db.execute("INSERT INTO game(result, money, userid) VALUES (?,?,?)",
                       newgame.result, loss, user_id)
            originalCashdict = db.execute("select cash from users where id = ?", user_id)
            originalCash = originalCashdict[0]['cash']
            newamount = originalCash + loss
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newamount, user_id)
        if result == "Player Wins!":
            profit = int(wagers[user_id])
            db.execute("INSERT INTO game(result, money, userid) VALUES (?,?,?)",
                       newgame.result, profit, user_id)
            originalCashdict = db.execute("select cash from users where id = ?", user_id)
            originalCash = originalCashdict[0]['cash']
            newamount = originalCash + profit
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newamount, user_id)
        if result == "Push":
            profit = 0
            db.execute("INSERT INTO game(result, money, userid) VALUES (?,?,?)",
                       newgame.result, profit, user_id)
        return render_template("result.html", playerimg=newgame.playerimg, dealerimg=newgame.dealerimg, result=result)


@app.route("/playgame")
@login_required
def wager():
    return render_template("playgame.html")


@app.route("/addmoney", methods=["GET", "POST"])
@login_required
def addmoney():
    """allow user to add money"""
    if request.method == "POST":
        # ensure user provides an input
        moneydict = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        if not request.form.get("addmoney"):
            return apology("Must provide a number", 400)
        # ensure user inputs a valid number
        money = moneydict[0]["cash"]
        money = int(money)
        additionalmoney = request.form.get("addmoney")
        try:
            int(additionalmoney)
        except ValueError:
            return apology("Must provide positive integer")
        additionalmoney = int(additionalmoney)
        if additionalmoney < 1:
            return apology("Must provide positive integer")
        money += additionalmoney
        db.execute("UPDATE users SET cash = ? WHERE id = ?", money, session["user_id"])
        return redirect("/")
    else:
        return render_template("addmoney.html")


@app.route("/")
@login_required
def index():
    count = db.execute(
        "SELECT count(id) FROM game WHERE userid = ?", session["user_id"]
    )
    if count[0]["count(id)"] < 1:
        return render_template("nogamesplayed.html")
    else:
        """show history of games and PnL"""
        # create dicts for each game, result, money-lost/won
        gamesplayed = db.execute(
            "SELECT count(id) FROM game WHERE userid = ?", session["user_id"])
        wl = db.execute(
            "SELECT result FROM game WHERE userid = ?", session["user_id"])
        pl = db.execute(
            "SELECT money FROM game WHERE userid = ?", session["user_id"])
        usertotalsql = db.execute(
            "SELECT cash from users where id = ?", session["user_id"]
        )
        # find total profit or loss
        PnLdict = db.execute(
            "SELECT sum(money) FROM game WHERE userid = ?", session["user_id"]
        )
        PnL = PnLdict[0]["sum(money)"]
        # find how much cash the user has
        cash = float(usertotalsql[0]["cash"])
        results = []
        # create a list of the total amount of games a user has played, e.g. game 1 game 2
        allgames = []
        for i in range(0, gamesplayed[0]['count(id)']):
            allgames.append(i + 1)

        # create a dict of the symbols, shares, prices, and total dicts
        if len(allgames) > 10:
            for i in range(len(allgames) - 10, len(allgames)):
                result = {
                    "Games": allgames[i],
                    "result": wl[i]['result'],
                    "profitloss": pl[i]['money']
                }
                results.append(result)
        else:
            for i in range(0, len(allgames)):
                result = {
                    "Games": allgames[i],
                    "result": wl[i]['result'],
                    "profitloss": pl[i]['money']
                }
                results.append(result)
        return render_template("index.html", results=results, cash=cash, PnL=PnL)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure re-entered password was submitted
        elif not request.form.get("confirmation"):
            return apology("must re-enter password", 400)
        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords must match", 400)
        # Ensure username does not exist, if not, adds the username and password to database
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 1:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
                    "username"), generate_password_hash(request.form.get("password"), method='scrypt', salt_length=16)
            )
        else:
            return apology("Username already exists", 400)
        # finds the user session id
        sessionid = db.execute(
            "SELECT id FROM users WHERE username = ?", request.form.get("username")
        )
        session["user_id"] = sessionid[0]['id']
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/resetpassword", methods=["GET", "POST"])
def resetpassword():
    """Reset password"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure re-entered password was submitted
        elif not request.form.get("new-password"):
            return apology("must re-enter password", 400)
        # Ensure username does exist
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 1:
            return apology("Username does not exist", 403)
        # Ensure passwords match
        passwords = db.execute(
            "select hash from users where username = ?", request.form.get("username"))
        password = passwords[0]["hash"]
        if not check_password_hash(
            password, request.form.get("password")
        ):
            return apology("must enter original password", 400)
        db.execute(
            "UPDATE users set hash = ? where username = ?", generate_password_hash(request.form.get(
                "new-password"), method='scrypt', salt_length=16), request.form.get("username")
        )
        # finds the user session id
        sessionid = db.execute(
            "SELECT id FROM users WHERE username = ?", request.form.get("username")
        )
        session["user_id"] = sessionid[0]['id']
        return redirect("/")
    else:
        return render_template("resetpassword.html")
