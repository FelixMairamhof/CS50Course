import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
db.execute("CREATE TABLE IF NOT EXISTS shares (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, symbol TEXT NOT NULL, share NUMERIC, cost NUMERIC, total NUMERIC);")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    # Fetch stocks and cash balance from the database
    stocks = db.execute("SELECT * FROM shares WHERE id = ?", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash_value = cash[0]["cash"] if cash else 0.0

    # Calculate total value of stocks
    total_stocks_value = sum(stock['total'] for stock in stocks)

    return render_template("index.html", stocks=stocks, cash=cash_value, total=total_stocks_value + cash_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Check if shares value is empty or not a valid number
        if not shares or not shares.replace('.', '', 1).isdigit():
            return apology("Shares must be a positive number", 400)

        # Convert shares to float for handling fractional shares
        shares = float(shares)

        # Check if shares is a non-positive number
        if shares <= 0:
            return apology("Shares must be a positive number", 400)

        # Check if shares is a fractional number
        if not shares.is_integer():
            return apology("Shares must be whole numbers", 400)

        # Retrieve stock information
        loockedUp = lookup(symbol)

        if not symbol or not loockedUp:
            return apology("Invalid symbol", 400)

        price_per_share = float(loockedUp["price"])
        total_cost = price_per_share * shares

        # Fetch the user's current cash from the database
        current_cash_query = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        if len(current_cash_query) != 1:
            return apology("Error fetching user's cash", 500)

        current_cash = current_cash_query[0]['cash']

        if current_cash < total_cost:
            return apology("Insufficient funds", 400)

        # Update the user's cash in the database after purchasing shares
        new_cash_balance = current_cash - total_cost
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash_balance, session["user_id"])

        # Calculate the purchased amount
        purchased_amount = total_cost

        # Redirect to the home page after purchase
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
def history():
    transactions = db.execute("SELECT * FROM shares WHERE id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        name = request.form.get("symbol")
        loockedUp = lookup(name)
        if loockedUp == None:
            return apology("Invalid Symbol", 400)
        price = loockedUp["price"]
        symbol = loockedUp["symbol"]
        # return {"price": price, "symbol": symbol}
        return render_template("quoted.html", name=symbol, symbol=symbol, price=price)
    else:
        return render_template("quote.html")


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

        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not password == confirmation:
            return apology("not the same passwords")

        # Fetch usernames from the database
        user_rows = db.execute("SELECT username FROM users")
        users = [row['username'] for row in user_rows]

        if name in users:
            return apology("Username already exists", 400)

        db.execute("INSERT INTO users (username,hash) VALUES (?,?)", name,
                   generate_password_hash(password, method='pbkdf2', salt_length=16))

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Please select a stock", 400)

        if not shares.isdigit() or int(shares) <= 0:
            return apology("Shares must be a positive integer", 400)

        stock = db.execute("SELECT share FROM shares WHERE id = ? AND symbol = ?", session["user_id"], symbol)

        if not stock or int(shares) > stock[0]["share"]:
            return apology("Invalid number of shares to sell", 400)

        price_per_share = lookup(symbol)["price"]
        total_earnings = price_per_share * int(shares)

        # Update cash balance after selling shares
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        new_cash_balance = user_cash + total_earnings
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash_balance, session["user_id"])

        # Deduct sold shares from the portfolio
        db.execute("UPDATE shares SET share = share - ? WHERE id = ? AND symbol = ?", int(shares), session["user_id"], symbol)

        # Log the transaction into history
        db.execute("INSERT INTO shares (id, symbol, share, cost, total) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], symbol, int(shares), price_per_share, total_earnings)

        return redirect("/")

    else:
        stocks = db.execute("SELECT DISTINCT symbol FROM shares WHERE id = ?", session["user_id"])
        return render_template("sell.html", stocks=stocks)
