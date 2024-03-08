import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///shoppingCart.db")




@app.route("/", methods=["GET", "POST"])
def index():
    db.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL);")
    if request.method == "POST":
        input = request.form.get("input")
        item = request.form.get("item")
        deleteAll = request.form.get("deleteAll")
        if not input and not item and not deleteAll:
            return redirect("/")
        elif input and not item:
            db.execute("INSERT INTO items ( name) VALUES (?);", input)
            return redirect("/")
        elif not input and item:
            db.execute("DELETE FROM items WHERE name = ?;", item)
            return redirect("/")
        elif deleteAll:
            db.execute("DELETE FROM items;")
            return redirect("/")
    else:
        drivers = db.execute("SELECT * FROM items;")
        return render_template("index.html", drivers=drivers)




