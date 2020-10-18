from flask import Flask, render_template, redirect, url_for, request, make_response, session
import airtable
import json
import svm
app = Flask(__name__)
app.secret_key = open("secret_key").read()

key = open("airtable_key").read()
db = airtable.Airtable('appvViVoTQrAVwGwR', 'hackgt', key)

PDFS = json.loads(open("pdfs.json").read())

@app.context_processor
def utils():
    def get_pdfs(pdfs=PDFS['articles'], number=200, width=3):
        ## todo: customize
        pdfs = pdfs[:number] # truncate amount

        for i in pdfs:
            i['abstract'] = ' '.join(i['abstract'].split(' ')[:50]) + ' ...'
        return [pdfs[i:i+width] for i in range(0, number, width)]

    return {'get_pdfs': get_pdfs, 'favorite': favorite}

def set_user(f, msg=True):
    session['user'] = f['username']
    if msg:
        session['message'] = f'Logged in as {f["username"]}'

    for user in db.get_all():
        f = user['fields']
        if f.get('username') == session['user']:
            session['likes'], session['dislikes'] = f.get('likes', ''), f.get('dislikes', '')
            session['favorites'] = f.get("favorites", '')
            return

@app.route('/favorite/<doi>')
def favorite(doi):
    session['favorites'] += ',' + '10.1101/' + doi
    session['favorites'] = ','.join(filter(bool, set(session['favorites'].split(',')))) # get rid of emptys/repeats
    db.update_by_field('username', session['user'], {'favorites': session['favorites']})
    return redirect(url_for('index'))

# Train the SVM and run the evaluations
@app.route('/recommended')
def recommendations(msg=None, error=None):
    if not session.get('likes'):
        set_user({'username': session['user']}, msg=False)

    if msg := session.get('message'):
        session['message'] = None

    if error := session.get('error'):
        session['error'] = None

    # Run the recommendation algorithm
    favs = session['favorites'].split(',')
    svm.train_svm(session['user'], favs)
    results = svm.eval_svm(session['user'])
    items = svm.doi2Item(results)
    return render_template('recommendations.html', recs = items, user=session.get('user'), error=error, message=msg)


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
    if not session.get('likes'):
        set_user({'username': session['user']}, msg=False)

    if msg := session.get('message'):
        session['message'] = None

    if error := session.get('error'):
        session['error'] = None

    return render_template('index.html', user=session.get('user'), error=error, message=msg)
