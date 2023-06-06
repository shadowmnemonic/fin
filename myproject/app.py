from flask import Flask, render_template, redirect, url_for
from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)
app.secret_key = '497732503295-1tpv5tsjlve97a0r1nbd6tik766kjmdc.apps.googleusercontent.com'  # Set a secret key for session management

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    # Retrieve the ID token from the POST request
    id_token_received = request.form.get('id_token')

    try:
        # Verify the ID token with Google
        id_info = id_token.verify_oauth2_token(id_token_received, requests.Request(), CLIENT_ID)

        if id_info['aud'] == CLIENT_ID:
            # ID token is valid, store user information in the session
            session['user_email'] = id_info['email']
            session['user_name'] = id_info['name']

            return redirect(url_for('currency_selection'))
        else:
            # Invalid ID token
            return 'Invalid ID token'

    except ValueError:
        # Error while verifying the ID token
        return 'Error while verifying ID token'

@app.route('/currency', methods=['GET', 'POST'])
def currency_selection():
    if request.method == 'POST':
        # Retrieve the selected currency from the form
        currency = request.form.get('currency')

        # Store the currency information in the session
        session['currency'] = currency

        return redirect(url_for('student_status_selection'))

    return render_template('currency.html')

@app.route('/student_status', methods=['GET', 'POST'])
def student_status_selection():
    if request.method == 'POST':
        # Retrieve the student status from the form
        student_status = request.form.get('student_status')

        # Store the student status information in the session
        session['student_status'] = student_status

        return redirect(url_for('dashboard'))

    return render_template('student_status.html')

@app.route('/dashboard')
def dashboard():
    # Retrieve user information from the session
    user_email = session.get('user_email')
    user_name = session.get('user_name')
    currency = session.get('currency')
    student_status = session.get('student_status')

    return render_template('dashboard.html', email=user_email, name=user_name, currency=currency, student_status=student_status)

if __name__ == '__main__':
    app.run(debug=True)
