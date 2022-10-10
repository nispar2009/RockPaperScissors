from crypt import methods
from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__)

# Establishing connection
connection = sqlite3.connect('rockpaperscissors.db')
cursor = connection.cursor()

# Creating tables
cursor.execute('CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE, onlineWins INT, computerWins INT)')
cursor.execute('CREATE TABLE IF NOT EXISTS challenges(id INTEGER PRIMARY KEY, user1 TEXT, user2 TEXT, input1 TEXT, input2 TEXT, winner TEXT)')

@app.route('/')
def index():
    connection = sqlite3.connect('rockpaperscissors.db')

    user = request.args.get('user')

    if user:
        user_in_db = cursor.execute('SELECT * FROM users WHERE username=?', (user,))
        
        if user_in_db:
            return render_template('index.html', user=user_in_db)

        # Signing up

        cursor.execute('INSERT INTO users VALUES (?, 0, 0)', (user,))
        connection.commit()

        new_user = cursor.execute('SELECT * FROM users WHERE username=?', (user,))

        connection.close()

        return render_template('index.html', user=new_user)

    # Signing in

    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)