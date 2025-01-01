import random
from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy database
users_db = {}
user_moods = {}  # Stores moods for each user

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_db.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Login successful!', category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', category='error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if username in users_db:
            flash('Username already exists, please choose another one.', category='error')
        elif password != confirm_password:
            flash('Passwords do not match. Please try again.', category='error')
        else:
            users_db[username] = {
                'email': email,
                'password': generate_password_hash(password)
            }
            user_moods[username] = []  # Initialize mood list for the user
            flash('Registration successful! Please log in.', category='success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    return render_template('dashboard.html', username=username)

@app.route('/mood-tracker', methods=['GET', 'POST'])
def mood_tracker():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    # Ensure the user has an entry in the user_moods dictionary
    if username not in user_moods:
        user_moods[username] = []

    if request.method == 'POST':
        date = request.form['date']
        mood = request.form['mood']
        # Ensure mood is not empty and date is valid
        if mood and date:
            user_moods[username].append({'date': date, 'mood': mood})
            flash(f'Mood "{mood}" saved for {date}!', category='success')
        else:
            flash('Please fill in both date and mood!', category='error')

    moods = user_moods.get(username, [])
    return render_template('mood_tracker.html', moods=moods)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', category='success')
    return redirect(url_for('home'))

# Mini Games Routes
@app.route('/mini_games')
def mini_games():
    return render_template('mini_games.html')

@app.route('/tictactoe')
def tictactoe():
    return render_template('tictactoe.html')

@app.route('/memory_match')
def memory_match():
    return render_template('memory_match.html')

@app.route('/hangman')
def hangman():
    return render_template('hangman.html')

# Daily Challenges Routes
@app.route('/daily_challenges')
def daily_challenges():
    challenges_data = {
        "riddles": [
            "I speak without a mouth and hear without ears. I have nobody, but I come alive with wind. What am I?",
            "The more of this there is, the less you see. What is it?",
            "I am not alive, but I grow; I don’t have lungs, but I need air; I don’t have a mouth, but water kills me. What am I?",
            "I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?",
            "What has to be broken before you can use it?",
            "I’m light as a feather, yet the strongest person can’t hold me for five minutes. What am I?",
            "What goes up but never comes down?",
            "The more you take, the more you leave behind. What am I?",
            "What can you break, even if you never pick it up or touch it?",
            "I’m found in the sky but never on land. I’m bright at night, but I fade at dawn. What am I?"
        ],
        "jokes": [
            "Why don't skeletons fight each other? They don't have the guts.",
            "What do you get if you cross a snowman and a vampire? Frostbite.",
            "Why don't programmers like nature? It has too many bugs.",
            "Why do cows wear bells? Because their horns don’t work.",
            "What do you call cheese that isn't yours? Nacho cheese.",
            "Why did the scarecrow win an award? Because he was outstanding in his field.",
            "Why don’t scientists trust atoms? Because they make up everything.",
            "What do you call fake spaghetti? An impasta.",
            "Why did the bicycle fall over? It was two-tired.",
            "What’s orange and sounds like a parrot? A carrot."
        ]
    }

    selected_riddle = random.choice(challenges_data["riddles"])
    selected_joke = random.choice(challenges_data["jokes"])

    return render_template('daily_challenges.html', riddle=selected_riddle, joke=selected_joke)

if __name__ == '__main__':
    app.run(debug=True)