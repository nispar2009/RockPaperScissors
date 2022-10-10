from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__)

# Establishing connection
connection = sqlite3.connect('rockpaperscissors.db')
cursor = connection.cursor()

# Creating tables
cursor.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, onlineWins INT, computerWins INT)')
cursor.execute('CREATE TABLE IF NOT EXISTS challenges(id INTEGER PRIMARY KEY, user1 TEXT, user2 TEXT, input1 TEXT, input2 TEXT, winner TEXT)')
connection.commit()

@app.route('/')
def index():
    connection = sqlite3.connect('rockpaperscissors.db')
    cursor = connection.cursor()

    user = request.args.get('user')

    if user:
        # Signing in
        
        if len((list(cursor.execute('SELECT * FROM users WHERE username=?', (user,))))) == 1:
            user_in_db = list(cursor.execute('SELECT * FROM users WHERE username=?', (user,)))[0]
            return render_template('index.html', user=user_in_db)

        else:

            # Signing up

            cursor.execute('INSERT INTO users(username, onlineWins, computerWins) VALUES(?, 0, 0)', (user,))
            connection.commit()

            new_user = list(cursor.execute('SELECT * FROM users WHERE username=?', (user,)))[0]

            # connection.close()

            return render_template('index.html', user=new_user)

    # Signing in

    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)