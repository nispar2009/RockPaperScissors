from flask import Flask, redirect, render_template, request
import sqlite3
import random

app = Flask(__name__)

# Establishing connection
connection = sqlite3.connect('rockpaperscissors.db')
cursor = connection.cursor()

# Creating tables
cursor.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, onlineWins INT, computerWins INT)')
cursor.execute('CREATE TABLE IF NOT EXISTS challenges(id INTEGER PRIMARY KEY, user1 TEXT, user2 TEXT, input1 TEXT, input2 TEXT)')
connection.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    connection = sqlite3.connect('rockpaperscissors.db')
    cursor = connection.cursor()

    if request.args.get('user'):
        user = request.args.get('user')
        # Signing in
        
        if len((list(cursor.execute('SELECT * FROM users WHERE username=?', (user,))))) == 1:
            user_in_db = list(cursor.execute('SELECT * FROM users WHERE username=?', (user,)))[0]
            return render_template('index.html', user=user_in_db)

        # Signing up

        cursor.execute('INSERT INTO users(username, onlineWins, computerWins) VALUES(?, 0, 0)', (user,))
        connection.commit()

        new_user = list(cursor.execute('SELECT * FROM users WHERE username=?', (user,)))[0]

        # connection.close()

        return render_template('index.html', user=new_user)

    # Signing in

    return render_template('signin.html')

# Practice matches (using Random)
@app.route('/practice', methods=['GET', 'POST'])
def practice():
    if request.method == 'GET':
        return render_template('practice.html', computer=random.choice(['r', 'p', 's']))

    win = request.form['win']
    if win == 'true':
        connection = sqlite3.connect('rockpaperscissors.db')
        cursor = connection.cursor()

        cursor.execute('UPDATE users SET computerWins=computerWins + 1 WHERE username=?', (request.args.get('user'),))

        connection.commit()

    return redirect(f'/?user={request.args.get("user")}')

@app.route('/challenge')
def challenge():
    connection = sqlite3.connect('rockpaperscissors.db')
    cursor = connection.cursor()

    user = request.args.get('user')
    all_users = list(cursor.execute('SELECT * FROM users WHERE username!=?', (user,)))
    challenges = list(cursor.execute('SELECT * FROM challenges WHERE user2=?', (user,)))

    return render_template('challenge.html', users=all_users, challenges=challenges, this_user=user)

@app.route('/createChallenge', methods=['POST'])
def createChallenge():
    choice = request.form['choice']
    user1 = request.form['user1']
    user2 = request.form['user2']

    connection = sqlite3.connect('rockpaperscissors.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO challenges(user1, user2, input1) VALUES (?, ?, ?)', (user1, user2, choice))

    connection.commit()
    connection.close()

    return redirect(f'/challenge?user={user1}')

@app.route('/react', methods=['POST'])
def react():
    choice2 = request.form['choice']
    current_challenge = request.form['challenge']
    user2 = request.form['user']

    connection = sqlite3.connect('rockpaperscissors.db')
    cursor = connection.cursor()

    cursor.execute('UPDATE challenges SET input2=? WHERE id=?', (choice2, current_challenge))

    choice1 = (list(cursor.execute('SELECT input1 FROM challenges WHERE id=?', (current_challenge))))[0][0]
    user1 = (list(cursor.execute('SELECT user1 FROM challenges WHERE id=?', (current_challenge))))[0]

    if choice2 == 'rock':
        if choice1 == 'scissors':
            cursor.execute('UPDATE users SET onlineWins=onlineWins+1 WHERE username=?', (user2,))
        if choice1 == 'paper':
            cursor.execute('UPDATE users SET onlineWins=onlineWins+1 WHERE username=?', user1)
    if choice2 == 'paper':
        if choice1 == 'rock':
            cursor.execute('UPDATE users SET onlineWins=onlineWins+1 WHERE username=?', (user2,))
        if choice1 == 'scissors':
            cursor.execute('UPDATE users SET onlineWins=onlineWins+1 WHERE username=?', user1)
    if choice2 == 'scissors':
        if choice1 == 'paper':
            cursor.execute('UPDATE users SET onlineWins=onlineWins+1 WHERE username=?', (user2,))
        if choice1 == 'rock':
            cursor.execute('UPDATE users SET onlineWins=onlineWins+1 WHERE username=?', user1)

    connection.commit()

    return redirect(f'/challenge?user={user2}')

if __name__ == '__main__':
    app.run(host='0.0.0.0')