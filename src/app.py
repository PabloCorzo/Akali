from flask import Flask,render_template,request,flash, session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
# import src.db_repository as db
import re
import hashlib

def hashPassword(password : str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

app = Flask(__name__,template_folder='src/templates',static_folder = 'src/static')

app.secret_key = 'key1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    _id = db.Column('id',db.Integer,primary_key = True)
    username = db.Column(db.String(32),unique = True,nullable = False)
    mail = db.Column(db.String(32),unique = True,nullable = True)
    password = db.Column(db.String(32),nullable = False)

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = hashPassword(password)
        
    def checkPassword(self):
        return Users.query.filter_by(username = self.username, password = self.password)

@app.route('/',methods = ['POST','GET'])
def home():
    return redirect(url_for('register'))

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'Post':
        username = request.form['username']
        password = request.form['password']
        # email = request.form['email']

        user = Users.query.filter_by(username = username).first()
        if user and user.checkPassword(password):
            session['username'] = user.username
            # session['email'] = user.email
            session['password'] = user.password
            return redirect(url_for('dashboard'))
        else:
            return render_template("login.html",error = "Invalid user")
    else:
        return render_template('login.html')
    
@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if email is None:
            email = ""
        user = Users.query.filter_by(username = username).first()
        if user:
            return render_template('index.html',error = 'user already registered')
        else:
            user = Users(username = username, password = password, email = email)
            db.session.add(user)
            db.session.commit()
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard',methods = ['POST','GET'])
def dashboard():
    return f"<h1>Dashboard</h1>"
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True,host = '0.0.0.0')