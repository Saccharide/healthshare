'''
Accounts:
(0) 0x06f47c9896f0e953af35320d61f020e8401002bc
(1) 0x7818c1e4713b6c45d0fd45cdba76089dbe37152d
(2) 0xc2d2f7152a8ed700d1cd08cb5cfbe4c7a1d9ce03
(3) 0xc164b6f48317178f3eb13467009b42e14300a780
(4) 0x55b82ed44a4beca98a346179485eaff6c32e9d1a
(5) 0x088dd259e0bc54385ff000c630d0da4a9dc29b3d
(6) 0xe56212c4fb7cb62c70bbbbd315f3ffcc597a0907
(7) 0x0d1a625f6ecbafd9d4bdf5255ccfebd23c612529
(8) 0x66121dff64ba79b034cb082c22c0895d49b909a3
(9) 0x3416ada4127128b7457138e8bcdd18020b645854

Private Keys:
(0) 30ad080b745feabb0b93d759aa49e59f7b349f01e7f2bfe69cfa20767e983cfa
(1) ab05c56bb662f502aa36bf3494949d5789c4c710958664c0fc397df7fd4dc860
(2) 224743028fbd1f108ec97e8d0e448b78ca2cf47db90792c39cde944856573485
(3) 41330c4b93512b5b6926159143f4930ea0ac96ef1d972261ae20620d01c99be9
(4) 5f8407f4d187f06b298b39fdfbc935e426b4882839fab636782a019cdaee21bd
(5) 23c0b1dd4c080446109cfcc1f23eb24b914bad5f70551ae38dcb37a8e9a73183
(6) 94c92685397831b9846bd12275fd2c1a8721d60bc8ac332aa5c630694565490d
(7) 2e5b11cf0841759913009fdf462bfc4ca8ed63412387d5f4cb66bf63e014ca61
(8) 552301299342183b7b57bb35ad2a0f11188be89ab762fb0ffc10b903048a8768
(9) f6eb1050cb3fec1795a1e6d450b53f929f8bd068cdfaeed7e052ebfb22c4a6e1



'''

from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from crypto import *
from werkzeug.utils import secure_filename
import os
import requests
import pexpect
import time


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# These variables are for testing, will be dynamic in the future when more APIs available
ACCOUNT_0 = "0x06f47c9896f0e953af35320d61f020e8401002bc"
ACCOUNT_1 = ""
BASE_URL = "http://localhost:3000"
CONNECTION_COMMAND = 'b localhost:52230'

def Upload_To_P2P(KEY, FILEPATH):
    child = pexpect.spawn('./dhtnode')
    child.expect('>>')
    child.sendline(CONNECTION_COMMAND)
    response = child.before
    print response
    time.sleep(2)
    child.expect('>>')
    put_command = 'p ' + KEY + " " +FILEPATH
    print(put_command)
    child.sendline(put_command)
    time.sleep(5)
    response = child.before
    print response

def Download_From_P2P(FILENAME):
    child = pexpect.spawn('./dhtnode')
    child.expect('>>')
    child.sendline(CONNECTION_COMMAND)
    response = child.before
    print response
    time.sleep(5)
    child.expect('>>')
    get_command = 'g ' + FILENAME
    print(get_command)
    child.sendline(get_command)
    response = child.before
    print response

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
        self.name = name
        self.birthday = birthdate

# API 1: GET FILES OF USERS
# Input: Blockchain Userid
# Output: List of files related to the user
def Get_User_Files(SERVER_URL, USER_ID):
    print("Query: " + "{}/getFiles?user_id={}".format(SERVER_URL, USER_ID))
    res = requests.get("{}/getFiles?user_id={}".format(SERVER_URL, USER_ID))
    ACCOUNT_1 = USER_ID
    return res.json()

# API 2: GET PUBLIC KEY OF USER
# Input: User ID of user
# Output: Public key of user
def Get_Public_Key(SERVER_URL, USER_ID):
    res = requests.get("{}/getPublicKey?user_id={}".format(SERVER_URL, USER_ID))
    return res.json()

# API 3: CREATE APPROVER MAPPING
# Input: File to be approved, approver user_id, encrypted secret share, file owner user id
# Output: Status message
def Create_Approver(SERVER_URL, FILENAME, APPROVER_ID, ENCRYPTED_SECRET_SHARE, OWNER_ID):
    res = requests.post("{}/setApprover".format(BASE_URL), json={
        "filename": FILENAME,
        "approver_id": APPROVER_ID,
        "encrypted_secret_share": ENCRYPTED_SECRET_SHARE,
        "user_id": OWNER_ID
    })
    return res.json()

# API 4: CHECK PENDING APPROVAL REQUESTS
def Approver_Check_Pending_Approval_Requests(SERVER_URL, USER_ID):
    res = requests.get("{}/getApprovableList?user_id={}".format(SERVER_URL, USER_ID))
    print("{}/getApprovableList?user_id={}".format(SERVER_URL, USER_ID))
    return res.json()

# API 5: GET APPROVED ENCRYPTED SECRET SHARES
def Get_Approver_Secret_Share(SERVER_URL, FILENAME, APPROVER_ID):
    res = requests.get("{}/getApproverSecret?filename={}&approver_id={}".format(SERVER_URL, FILENAME, APPROVER_ID))
    return res.json()

# API 6: APPROVE REQUEST
def Approve_Request(SERVER_URL, FILENAME, REQUESTOR_ID, ENCRYPTED_SECRET_SHARE, OWNER_ID):
    print("{}/approve".format(SERVER_URL))
    print("filename:" + str(FILENAME) + " requestor:" + str(REQUESTOR_ID) + ", encrypted_share: " + str(ENCRYPTED_SECRET_SHARE) + ", user_id: " + str(OWNER_ID))
    res = requests.post("{}/approve".format(SERVER_URL), json={
        "filename": FILENAME,
        "requestor": REQUESTOR_ID,
        "encrypted_share": ENCRYPTED_SECRET_SHARE,
        "user_id": OWNER_ID
    })
    return res.json()

# API 7: ASSOCIATE PUBLIC KEY WITH USER
def Associate_Public_Key(SERVER_URL, USER_ID, PUBLIC_KEY):
    res = requests.post("{}/setPublicKey".format(SERVER_URL), json={
        "user_id": USER_ID,
        "public_key": PUBLIC_KEY
    })
    return res.json()

# API 8: GET LIST OF USERS FILES
def Add_User_Files(SERVER_URL, USER_ID, FILENAME):
    res = requests.post("{}/addFile".format(SERVER_URL), json={
        "user_id": USER_ID,
        "file_name": FILENAME
    })
    return res.json()

# API 9: GET ETH ADDRESS
def Get_ETH_Address(SERVER_URL, NAME, BIRTHDATE):

    if "Alice" in NAME:
        return "0x7818c1e4713b6c45d0fd45cdba76089dbe37152d"
    if "Elgin" in NAME:
        return "0x06f47c9896f0e953af35320d61f020e8401002bc"
    if "Cow" in NAME:
        return "0xc2d2f7152a8ed700d1cd08cb5cfbe4c7a1d9ce03"
    res = requests.get("{}/getAddressFromDetails?name={}&birthday={}".format(SERVER_URL, NAME, BIRTHDATE))
    print(res)
    return res.json()['data'].lower()

# API 10: CREATING A PATIENTS ETH ADDRESS
def Create_ETH_Address(SERVER_URL, NAME, BIRTHDATE, ADDRESS):
    res = requests.post("{}/setDetails".format(SERVER_URL), json={
        "name": NAME,
        "birthday": BIRTHDATE,
        "user_id": ADDRESS
    })
    return res.json()

# API 11: REQUEST AUTHORIZATION TO VIEW FILE
def Request_Authorization(SERVER_URL, FILENAME, REQUESTOR_ID):
    res = requests.post("{}/requestFile".format(SERVER_URL), json={
        "filename": FILENAME,
        "user_id": REQUESTOR_ID
    })
    return res.json()

# API 12: DUPLICATE OF API 1

# API 13: DELETE FILE
def Delete_File(SERVER_URL, FILENAME, REQUESTOR_ID):
    res = requests.post("{}/removeFile".format(SERVER_URL), json={
        "filename": FILENAME,
        "user_id": REQUESTOR_ID
    })
    return res.json()

# API 14: GET A LIST OF A SECRETE SHARES FOR FILES THAT WERE REQUESTED PREVIOUSLY
def Get_List_Of_Files_With_Secret_Share(SERVER_URL,USER_ID):
    res = requests.get("{}/getApprovedListSecrets?user_id={}".format(SERVER_URL, USER_ID))
    return res.json()



@app.route('/approve', methods=['GET', 'POST'])
def approve():
    """View Form"""
    file_list = Approver_Check_Pending_Approval_Requests(BASE_URL,ACCOUNT_0)

    items_list = []

    for file in file_list["data"]:
        print(file)
        if file != '':
            item = {'File Name': file, 'Actions': {'icon': 'fa fa-plus', 'text': 'Approve', 'link': 'approve_file?filename=' + file}}
            items_list.append(item)
            
    return render_template('approve.html', data=session['username'], columns=['File Name', 'Actions'], items=items_list)


@app.route('/view/authorize', methods=['GET', 'POST'])
def authorize():
    filename = request.args.get('filename')
    print(filename)
    return render_template('authorize.html', filename=filename)

@app.route('/approve_file', methods=['GET'])
def approve_file():
    filename = request.args.get('filename')
    print("Approving File: " + filename)

    # get the approver secret share
    secret_share = eval(Get_Approver_Secret_Share(BASE_URL, filename, ACCOUNT_0)['data'])[1]

    print(secret_share)

    Approve_Request(BASE_URL, filename, ACCOUNT_0, secret_share, ACCOUNT_1)

    return render_template("success.html", name = filename)  

@app.route('/authorize-request', methods=['POST'])
def authorize_request():
    name = []
    birthdate = []
    share_count = 0
    authorizer_id = []

    required = request.form['required']
    filename = request.form['filename']

    for key in request.form.keys():
        if 'name' in key:
            name.append(request.form[key])
        if 'birthdate' in key:
            birthdate.append(request.form[key])

    for single_name, single_birthdate in zip(name,birthdate):
        authorizer_id.append(Get_ETH_Address(BASE_URL, single_name, single_birthdate))
        share_count = share_count + 1

    print("Share Count: " + str(share_count))
    print("Required: " + required)
    print(authorizer_id)

    secret, shares = make_random_shares(int(required), share_count)

    for single_authorizer_id, single_share in zip(authorizer_id,shares):
        print("Authorizer: " + single_authorizer_id + " ,Share: " + str(single_share))
        print(Create_Approver(BASE_URL, filename, single_authorizer_id, str(single_share), ACCOUNT_0)['data'])

    return redirect(url_for('view'))

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

                # For debuging purposes
                print("name: " + name)
                global ACCOUNT_0
                if 'Alice' in name:
                    ACCOUNT_0 = "0x7818c1e4713b6c45d0fd45cdba76089dbe37152d"
                    print("ACCOUNT_0 set to: " + ACCOUNT_0)

                if 'Cow' in name:
                    ACCOUNT_0 = "0xc2d2f7152a8ed700d1cd08cb5cfbe4c7a1d9ce03"
                    print("ACCOUNT_0 set to: " + ACCOUNT_0)

                return redirect(url_for('home'))
            else:
                return 'Dont Login'
        except:
            return "Dont Login"

@app.route('/view/', methods=['GET', 'POST'])
def view():
    """View Form"""
    file_list = Get_User_Files(BASE_URL,ACCOUNT_0)

    items_list = []

    for file in file_list["data"]:
        print(file)
        if file != '':
            item = {'File Name': file, 'Actions': {'icon': 'fa fa-plus', 'text': 'Authorize', 'link': 'authorize?filename=' + file}}
            items_list.append(item)
            
    return render_template('view.html', data=session['username'], columns=['File Name', 'Actions'], items=items_list)

@app.route('/uploadfile/', methods=['GET', 'POST'])
def uploadfile():
    return render_template('upload.html')

@app.route('/request/', methods=['GET'])
def request_page():
    return render_template('request.html')

@app.route('/requestuser/', methods=['POST'])
def request_user():
    name = request.form['name']
    birthdate = request.form['birthdate']

    user_id = Get_ETH_Address(BASE_URL, name, birthdate)
    print("User ID:" + user_id)


    file_list = Get_User_Files(BASE_URL,user_id)

    items_list = []

    for file in file_list["data"]:
        print(file)
        if file != '':
            item = {'File Name': file, 'Actions': {'icon': 'fa fa-plus', 'text': 'Request', 'link': 'request_file?filename=' + file}}
            items_list.append(item)
            
    return render_template('view.html', data=session['username'], columns=['File Name', 'Actions'], items=items_list)

@app.route('/requestuser/request_file/', methods=['GET'])
def request_file():
    filename = request.args.get('filename')
    print("File requested: " + filename, ", Requestor: " + ACCOUNT_0)

    global ACCOUNT_0

    print(Request_Authorization(BASE_URL, filename, ACCOUNT_0)['data'])

    return redirect(url_for('home'))

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

        # TO BE DONE, for now take the account ID as ACCOUNT_0

        # associate public key

        print("Associating Public Key:")

        res = requests.post("{}/setPublicKey".format(BASE_URL), json={
            "user_id": ACCOUNT_0,
            "public_key": public_key
        })


        print(res.json()['data'])
        print()


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
        hashed_name = secure_filename(str(secret))
        obs_filname = os.path.join(uploads_dir, hashed_name)

        f.save(obs_filname)

        print("Adding file to blockchain")
        res = requests.post("{}/addFile".format(BASE_URL), json={
            "user_id": ACCOUNT_0,
            "file_name": hashed_name
        })

        print(res.json()['data'])
        print()

        print("Adding file to p2p")

        Upload_To_P2P(hashed_name, obs_filname)



        return render_template("success.html", name = str(secret))  

if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
    
