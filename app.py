from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__)

# Establishing connection
connection = sqlite3.connect("rockpaperscissors.db")
cursor = connection.cursor()

# Creating tables
cursor.execute("CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE, onlineWins INT, computerWins INT)")
cursor.execute("CREATE TABLE IF NOT EXISTS challenges(user1 TEXT, user2 TEXT, input1 TEXT, input2 TEXT, winner TEXT)")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)