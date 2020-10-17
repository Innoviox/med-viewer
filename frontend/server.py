from flask import Flask, render_template, redirect, url_for, request, make_response, session
import airtable

app = Flask(__name__)
app.secret_key = open("secret_key").read()

key = open("airtable_key").read()
db = airtable.Airtable('appvViVoTQrAVwGwR', 'hackgt', key)

@app.route('/logout', methods=['POST'])
def logout():
    session['user'] = None
    session['message'] = f'Logged out'

    return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    for user in db.get_all():
        f = user['fields']
        if f['username'] == username and f['password'] == password:
            session['user'] = username
            session['message'] = f'Logged in as {username}'
            return redirect(url_for('index'))

    session['error'] = 'User not found'
    return redirect(url_for('index'))

@app.route('/create', methods=['POST'])
def create():
    username = request.form['username']
    password = request.form['password']

    for user in db.get_all():
        f = user['fields']
        if f['username'] == username:
            session['error'] = f'Username {username} already exists'
            return redirect(url_for('index'))

    session['user'] = username
    session['message'] = f'Logged in as {username}'

    db.insert({'username': username, 'password': password})
    return redirect(url_for('index'))

@app.route('/')
def index(msg=None, error=None):
    if msg := session.get('message'):
        session['message'] = None

    if error := session.get('error'):
        session['error'] = None

    return render_template('index.html', user=session.get('user'), error=error, message=msg)