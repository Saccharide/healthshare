'''
Testing Data:

Accounts:
(0) 0xc69f09325d43e67785bf517211794794e0747c61
(1) 0x1e734adb5198006d7c9b1644f45c8f5991f64346
(2) 0x41e7b4fa399e9f8130b6977858580268f0144d83
(3) 0xfe53dbdf4ad769910a13ed729fbbcb22185508bd
(4) 0xf34e99232a843825ad39b605b25a45c267959a08
(5) 0x9d9c94c73a0d80205b4993e9fbf172b2cf5abeaf
(6) 0x747c787b1ba1d272293fa505415123b8441b6f1c
(7) 0xa115a68641bf3c3f795448dd3c739f112c15414e
(8) 0x96f748a00a795a23076e0f3f70f88eccc8fe2230
(9) 0x1d7834c4b89155eed343d33c50fb4bbd2150e892

Private Keys:
(0) 50ad642cfc5629ee06d2c94288bca68121c84f5e3ac9f2a280400a15c47fc2aa
(1) 921cd8be40accc2b61d93078a24a5ddb7971261f12f0e1e3b7650984a50a45df
(2) 6dd8ddd4ddc3b27a0fa6be0f8bc96486d2175dbe1221f2e1ed5d8fe21c7e16cd
(3) 09e05ce2489831935c6d7c573ef3ad45bbe9bdead9b9cb1449a9a002c7249480
(4) f9683132cb389112f88e756935deabfefb034b246f2b974f9d7f7ac6ead4c75d
(5) 3f007ff7e53b6b436c9604fe0c7c28f7b680a1e9caa5f3ca2acc4c8271dbae8a
(6) 8f42bfc685f9de2332c8991090060fa0c7b10265fe02fdd634a50c98b7455310
(7) 7967c1705c9f3ce84c1d437f510ac34a0c7a87efcddce8cd01266c8d8dcdfac7
(8) 43dd2926131dcc58d3238f83a7a61f9d04d5851f7e71ece473634a5dd8a5aa8f
(9) b01851c2785fbea0bbd4e814a30237f1e3e0b1d1a1cd7cdcd8d8169a4eedbc6e


'''

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
ACCOUNT_0 = "0xc69f09325d43e67785bf517211794794e0747c61"
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

    def __init__(self, username, password, private_key, public_key, name, birthdate):
        self.username = username
        self.password = password
        self.private_key = private_key
        self.public_key = public_key
        #set for testing purposes
        self.name = name
        self.birthday = birthdate

# API 1: GET FILES OF USERS
# Input: Blockchain Userid
# Output: List of files related to the user
def API_1(SERVER_URL, USER_ID):
    print("API 1 called:")
    print("{}/getFiles?user_id={}".format(SERVER_URL, USER_ID))
    res = requests.get("{}/getFiles?user_id={}".format(SERVER_URL, USER_ID))
    return res.json()

# API 2: GET PUBLIC KEY OF USER
# Input: User ID of user
# Output: Public key of user
def API_2(SERVER_URL, USER_ID):
    res = requests.get("{}/getPublicKey?user_id={}".format(SERVER_URL, USER_ID))
    return res.json()

# API 3: CREATE APPROVER MAPPING
# Input: File to be approved, approver user_id, encrypted secret share, file owner user id
# Output: Status message
def API_3(SERVER_URL, FILENAME, APPROVER_ID, ENCRYPTED_SECRET_SHARE, OWNER_ID):
    res = requests.post("{}/setApprover".format(BASE_URL), json={
        "filename": FILENAME,
        "approver_id": APPROVER_ID,
        "encrypted_secret_share": ENCRYPTED_SECRET_SHARE,
        "user_id": OWNER_ID
    })
    return res.json()

# API 4: CHECK PENDING APPROVAL REQUESTS
def API_4(SERVER_URL, USER_ID):
    res = requests.get("{}/getApprovableList?user_id={}".format(SERVER_URL, USER_ID))
    return res.json()

# API 5: GET APPROVED ENCRYPTED SECRET SHARES
def API_5(SERVER_URL, FILENAME, APPROVER_ID):
    res = requests.get("{}/getApproverSecret?filename={}&approver_id={}".format(SERVER_URL, FILENAME, APPROVER_ID))
    return res.json()

# API 6: APPROVE REQUEST
def API_6(SERVER_URL, FILENAME, REQUESTOR_ID, ENCRYPTED_SECRET_SHARE, OWNER_ID):
    res = requests.post("{}/approve".format(SERVER_URL), json={
        "filename": FILENAME,
        "requestor": REQUESTOR_ID,
        "encrypted_share": ENCRYPTED_SECRET_SHARE,
        "user_id": OWNER_ID
    })
    return res.json()

# API 7: ASSOCIATE PUBLIC KEY WITH USER
def API_7(SERVER_URL, USER_ID, PUBLIC_KEY):
    res = requests.post("{}/setPublicKey".format(SERVER_URL), json={
        "user_id": USER_ID,
        "public_key": PUBLIC_KEY
    })
    return res.json()

# API 8: GET LIST OF USERS FILES
def API_8(SERVER_URL, USER_ID, FILENAME):
    res = requests.post("{}/addFile".format(SERVER_URL), json={
        "user_id": USER_ID,
        "file_name": FILENAME
    })
    return res.json()

# API 9: GET ETH ADDRESS
def API_9(SERVER_URL, NAME, BIRTHDATE):
    res = requests.get("{}/getAddressFromDetails?name={}&birthday={}&user_id={}".format(SERVER_URL, NAME, BIRTHDATE))
    return res.json()

# API 10: CREATING A PATIENTS ETH ADDRESS
def API_10(SERVER_URL, NAME, BIRTHDATE, ADDRESS):
    res = requests.post("{}/setDetails".format(SERVER_URL), json={
        "name": NAME,
        "birthday": BIRTHDATE,
        "user_id": ADDRESS
    })
    return res.json()

# API 11: REQUEST AUTHORIZATION TO VIEW FILE
def API_11(SERVER_URL, FILENAME, REQUESTOR_ID):
    res = requests.post("{}/requestFile".format(SERVER_URL), json={
        "filename": FILENAME,
        "user_id": REQUESTOR_ID
    })
    return res.json()

# API 12: DUPLICATE OF API 1

# API 13: DELETE FILE
def API_13(SERVER_URL, FILENAME, REQUESTOR_ID):
    res = requests.post("{}/removeFile".format(SERVER_URL), json={
        "filename": FILENAME,
        "user_id": REQUESTOR_ID
    })
    return res.json()

# API 14: GET A LIST OF A SECRETE SHARES FOR FILES THAT WERE REQUESTED PREVIOUSLY
def API_14(SERVER_URL,USER_ID):
    res = requests.get("{}/getApprovedListSecrets?user_id={}".format(SERVER_URL, USER_ID))
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
    file_list = API_1(BASE_URL,ACCOUNT_0)

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
            name=request.form['name'],
            birthdate=request.form['birthdate'],
            private_key=private_key,
            public_key=public_key)

        db.session.add(new_user)
        db.session.commit()

        return redirect("/", code=302)
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
        
        uploads_dir = os.path.join(app.instance_path, 'uploads')
        obs_filname = os.path.join(uploads_dir,secure_filename(str(secret)))

        f.save(obs_filname)

        

        return render_template("success.html", name = str(secret))  

if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
    
