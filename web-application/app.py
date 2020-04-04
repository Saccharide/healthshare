from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from crypto import *
from werkzeug.utils import secure_filename
import os
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# These variables are for testing, will be dynamic in the future when more APIs available
ACCOUNT_0 = "0x06f47c9896f0e953af35320d61f020e8401002bc"
BASE_URL = "http://localhost:3000"

class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    private_key = db.Column(db.String(200))
    public_key = db.Column(db.String(200))
    name = db.Column(db.String(80))
    birthday = db.Column(db.String(80))

    def __init__(self, username, password, private_key, public_key):
        self.username = username
        self.password = password
        self.private_key = private_key
        self.public_key = public_key
        #set for testing purposes
        self.name = username
        self.birthday = "01/01/1990"

# API 1: GET FILES OF USERS
# Input: Blockchain Userid
# Output: List of files related to the user
def API_1():
    res = requests.get("{}/getFiles?user_id={}".format(BASE_URL, ACCOUNT_0))
    return res.json()

@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            username = getname(request.form['username'])
            return render_template('index.html', data=self.username)
        return render_template('index.html', data=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
            data = User.query.filter_by(username=name, password=passw).first()
            if data is not None:
                session['logged_in'] = True
                session['username'] = request.form['username']
                return redirect(url_for('home'))
            else:
                return 'Dont Login'
        except:
            return "Dont Login"

@app.route('/view/', methods=['GET', 'POST'])
def view():
    """View Form"""
    file_list = API_1()

    items_list = []

    for file in file_list["data"]:
        print(file)
        if file != '':
            item = {'File Name': file, 'Date Created': '-', 'Actions': {'icon': 'fa fa-plus', 'text': 'Open'}}
            items_list.append(item)

    #items_list = [{'File Name': 'HelloWorld.zip', 'Date Created': '24/11/2020', 'Actions': {'icon': 'fa fa-plus', 'text': 'Open'}},
    #      {'File Name': 'WorldHello.zip', 'Date Created': '30/11/2020', 'Actions': {'icon': '#', 'text': 'Open'}}]
    return render_template('view.html', data=session['username'], columns=['File Name', 'Date Created', 'Actions'], items=items_list)

@app.route('/uploadfile/', methods=['GET', 'POST'])
def uploadfile():
    return render_template('upload.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register Form"""
    if request.method == 'POST':

        private_key, public_key = generate_RSA()
        print("Private key:" + str(private_key))
        print("Public key:" + str(public_key))

        new_user = User(
            username=request.form['username'],
            password=request.form['password'],
            private_key=private_key,
            public_key=public_key)

        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')


@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        secret, shares = make_random_shares(1, 1)
          
        #f.save(f.filename)
        uploads_dir = os.path.join(app.instance_path, 'uploads')
        obs_filname = os.path.join(uploads_dir,secure_filename(str(secret)))

        f.save(obs_filname)    
        return render_template("success.html", name = str(secret))  

if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
    
