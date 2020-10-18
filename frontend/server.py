from flask import Flask, render_template, redirect, url_for, request, make_response, session
import airtable
import json

app = Flask(__name__)
app.secret_key = open("secret_key").read()

key = open("airtable_key").read()
db = airtable.Airtable('appvViVoTQrAVwGwR', 'hackgt', key)

PDFS = json.loads(open("pdfs.json").read())

@app.context_processor
def utils():
    def get_pdfs(number=6, width=3):
        ## todo: customize
        pdfs = PDFS['articles'][:number]
        for i in pdfs:
            i['abstract'] = ' '.join(i['abstract'].split(' ')[:50]) + ' ...'
        return [pdfs[i:i+width] for i in range(0, number, width)]
    return {'get_pdfs': get_pdfs}

def set_user(f):
    session['user'] = f['username']
    session['message'] = f'Logged in as {f["username"]}'

    for user in db.get_all():
        f = user['fields']
        if f['username'] == session['user']:
            session['likes'], session['dislikes'] = f['likes'], f['dislikes']
            return

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
            set_user(f)
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

    f = {'username': username, 'password': password}

    set_user(f)
    db.insert(f)
    return redirect(url_for('index'))

@app.route('/')
def index(msg=None, error=None):
    if msg := session.get('message'):
        session['message'] = None

    if error := session.get('error'):
        session['error'] = None

    return render_template('index.html', user=session.get('user'), error=error, message=msg)