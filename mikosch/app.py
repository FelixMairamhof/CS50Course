import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///drivers.db")

@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")

@app.route("/drive", methods=["GET"])
def drive():
    return render_template("submit.html")

@app.route("/", methods=["GET", "POST"])
def index():
    db.execute("CREATE TABLE IF NOT EXISTS drivers (name TEXT NOT NULL, location TEXT NOT NULL, time INTEGER NOT NULL, seats INTEGER NOT NULL);")

    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")
        time = request.form.get("time")
        seats = request.form.get("seats")
        passenger = request.form.get("passenger")

        if not name or not location or not time or not seats:
            return redirect("/error")

        if  passenger:

            db.execute("CREATE TABLE IF NOT EXISTS ? (name TEXT NOT NULL);",name)
            db.execute("INSERT INTO ? (name) VALUES (?);", name,passenger)
            return redirect("/")
        else:
            db.execute("INSERT INTO drivers (name,location,time,seats) VALUES (?,?,?,?);", name,location,time,seats)
            return redirect("/")

    else:
        drivers = db.execute("SELECT * FROM drivers;")
        return render_template("index.html", drivers=drivers)




