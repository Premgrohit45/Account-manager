from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_sqlalchemy import SQLAlchemy
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from flask_sqlalchemy import SQLAlchemy
from waitress import serve

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for flash messages

# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'acoounts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialize SQLALchemy
db = SQLAlchemy(app)
# Define Account model
class tblregister(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(256), nullable=False)  # Stores encrypted password
    masterPassword = db.Column(db.String(256), nullable=False) 
    mobile = db.Column(db.String(20), nullable=True)
    

    def repr(self):
        return f'<register {self.account_name}>'
    
# Define Account model
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(100), nullable=False)
    account_url = db.Column(db.String(200), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(256), nullable=False)  # Stores encrypted password
    mobile_number = db.Column(db.String(20), nullable=True)
    narration = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), nullable=False)
    tblregister_id = db.Column(db.Integer, nullable=False)
    def repr(self):
        return f'<Account {self.account_name}>'
    
    # Create database tables
with app.app_context():
     db.create_all()

@app.route('/')
def index():
    # credentials = Credential.query.all()
     return render_template('index.html')

# @app.route('/register', methods= ['GET','POST'])
# def register():
#     return render_template('register.html')

@app.route('/credentials', methods=['GET', 'POST'])
def credentials(): 
    if 'user_id' not in session:
        flash("Please log in to view accounts.", "warning")
        return redirect(url_for('login'))
    if request.method == 'POST':
        print("Credentials POST request received")
        accountName = request.form.get('accountName')
        accountUrl = request.form.get('accountUrl')
        accountType = request.form.get('accountType')
        username = request.form.get('username')
        password = request.form.get('password')
        mobileNumber = request.form.get('mobileNumber')
        priority = request.form.get('priority')
        narration = request.form.get('narration')
        r_id = session['user_id']  # Get the user ID from the session
        print("Account ID 111:", r_id)
        # Basic validation
        # if not accountName or not accountUrl or not accountType or not username or not password:
        #     flash("Please fill all required fields.", "danger")
        #     return redirect(url_for('credentials'))
        print("Account ID 222:", r_id)
        # Create and save account
        add_account = Account(
            account_name=accountName,
            account_url=accountUrl,
            account_type=accountType,
            username=username,
            password=password,
            mobile_number=mobileNumber if mobileNumber else None,
            narration=narration if narration else None,
            priority=priority,
            tblregister_id=r_id  # Associate with the logged-in user
        )
        db.session.add(add_account)
        db.session.commit()
        flash("Credential saved successfully!", "success")
        return redirect(url_for('viewaccount'))  # Redirect to view page after successful add

    return render_template('credentials.html')  # This only runs for GET request



@app.route('/register', methods=['GET', 'POST'])
def register():
    # print("Hellooooooo.......")
    if request.method == 'POST':
        accountName = request.form.get('accountName')
        username = request.form.get('username')
        password = request.form.get('password')
        mobile = request.form.get('mobile')
        masterPassword = request.form.get('masterPassword')

        existing_user = tblregister.query.filter_by(username=username).first()

        if existing_user:
            flash('username/email already exist','error')
            return render_template('register.html')

        
         # Create new account
        add_account = tblregister(
            account_name=accountName,
            username=username,
            password=password,
            mobile=mobile if mobile else None,
            masterPassword=masterPassword
            )
   
   #     # Save to database
        db.session.add(add_account)
        db.session.commit()
        flash('Form submitted successfully!', 'success')
        print('save success..........')
        print(accountName)
        print(username)
        print(password)
        print(mobile)
        print(masterPassword)

    return render_template('register.html')


@app.route('/viewaccount')
def viewaccount():
    if 'user_id' not in session:
        flash("Please log in to view accounts.", "warning")
        return redirect(url_for('login'))
    log_name = session['username']
    user_id = session['user_id']
    print(session['user_id'])
    # accounts = Account.query.all()
    accounts = Account.query.filter_by(tblregister_id=user_id).all()
    return render_template('viewaccount.html', accounts=accounts, log_name=log_name)
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/edit/<int:account_id>', methods=['GET', 'POST'])
def edit_account(account_id):
    account = Account.query.get_or_404(account_id)

    if request.method == 'POST':
        account.account_name = request.form.get('accountName')
        account.account_url = request.form.get('accountUrl')
        account.account_type = request.form.get('accountType')
        account.username = request.form.get('username')
        account.password = request.form.get('password')
        account.mobile_number = request.form.get('mobileNumber')
        account.narration = request.form.get('narration')
        account.priority = request.form.get('priority')

        db.session.commit()
        flash('Account updated successfully.', 'success')
        return redirect(url_for('viewaccount'))

    return render_template('edit_account.html', account=account)

@app.route('/delete/<int:account_id>', methods=['POST'])
def delete_account(account_id):
    account = Account.query.get_or_404(account_id)
    db.session.delete(account)
    db.session.commit()
    flash('Account deleted successfully.', 'success')
    return redirect(url_for('viewaccount'))

@app.route('/login', methods=['GET', 'POST'])
# @app.route('/login')
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')        
        masterPassword = request.form.get('masterPassword')
        # Select * from tblregister where username = username and password = password
        # ORM(Object Relational Model) flask_sqlalchemy
        user = tblregister.query.filter(
            (tblregister.username == username) & (tblregister.password == password) 
        ).first()
        if user:
            if(user.masterPassword == masterPassword):
                m1 = "Welcome to Account Mgr: " + user.account_name
                m2 = "Your Master Psw: " + user.masterPassword
                print(m1,m2)
                print("Login Success.")
            else:
                print("Login Fail.")

        if user:
            session['user_id'] = user.id
            session['username'] = user.account_name
            flash(f"Welcome, {user.account_name}!", "success")
            return redirect(url_for("viewaccount")) # Redirect to account page after login

        else:
            flash("Invalid credentials or master password.", "error")
            return redirect(url_for("login"))                

    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/B')
def B():
    return render_template('B.html')

@app.route('/home')
def home():
    return render_template('home.html')
    
if __name__ == '__main__':
    # app.run(debug=True)
    serve(app, host="0.0.0.0", port=8000,threads=8)


    # app.run(debug=True)