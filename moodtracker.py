from app import app
from flask import flash, redirect, render_template, request, session, url_for

@app.route('/moodtracker', methods=['GET', 'POST'])
def moodtracker():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Capture the user's mood
        mood = request.form['mood']
        date = request.form['date']  # Capture the selected date

        # In a real app, you would save this data to a database.
        # For now, just flash a message.
        flash(f"Mood for {date}: {mood} saved!", category='success')

    return render_template('moodtracker.html')
