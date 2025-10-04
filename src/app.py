from flask import Flask,render_template,request,flash, session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
# import src.db_repository as db
# import loginscripts,hobby
import os
import sys
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import re
import hashlib

import sys
sys.path.append("../src")



load_dotenv()
app = Flask(__name__, template_folder='templates', static_folder='static')
db = SQLAlchemy()
app.secret_key = 'key1'

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_port = os.getenv("DB_PORT")

db_uri = f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
print(f"DEBUG: Conectando a la base de datos con la URI: {db_uri}")
# Construye la URI de la base de datos de forma segura
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class Users(db.Model):
    _id = db.Column('id',db.Integer,primary_key = True)
    username = db.Column('username',db.String(32),unique = True,nullable = False)
    email = db.Column('email',db.String(32),unique = True,nullable = True)
    password = db.Column('password',db.String(32),nullable = False)

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = self.hashPassword(password)

    def hashPassword(self,password : str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    def checkPassword(self,username, password):
        return Users.query.filter_by(username = username, password = password)

class Hobby(db.Model):
    _hobby_id = db.Column('hobby_id',db.Integer,primary_key = True)
    name = db.Column('name',db.String(100),unique = False,nullable = False)
    user_id = db.Column('user_id',db.Integer,unique = False,nullable = True)
    satisfaction_level = db.Column('satisfaction_level',db.Integer,nullable = True)
    ability = db.Column('ability',db.String(100),nullable = True)
    time = db.Column('time',db.Time,nullable = True)

    def __init__(self,name,user_id,satisfaction_level,ability,time):
        self.name = name
        self.user_id = user_id
        self.satisfaction_level = satisfaction_level
        self.ability = ability
        self.time = time

@app.route('/',methods = ['POST','GET'])
def home():
    return redirect(url_for('login'))

@app.route('/login', methods = ['GET','POST'])
def login():
    print(f"Login iniciado con metodo: {request.method}")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # email = request.form['email']
        print(f'username {username} password {password}')
        user = Users.query.filter_by(username = username).first()
        print("Supposed 'test' password encryption: {9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08}")
        print(f'Actual value: {user.checkPassword(username,password)}')
        print(user.hashPassword(password) == '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08')
        if user and user.checkPassword(username,password):
            session['username'] = user.username
            # session['email'] = user.email
            session['id'] = user._id
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
            return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout', methods = ['POST','GET'])
def logout():
    session['id'] = None
    session['username'] = None
    return redirect(url_for('/'))

@app.route('/dashboard',methods = ['POST','GET'])
def dashboard():
    return f"<h1>Dashboard</h1>"

@app.route("/hobby",methods = ["POST","GET"])
def create_hobby():
    errors = []
    # if not session.get('loggedin'):
    #     return redirect(url_for('login'))
    #

    # if not user_id:
    #     return redirect(url_for('login'))

    if request.method == "POST":
        name = request.form["name"].strip()
        satisfaction_level = request.form["satisfaction_level"].strip()
        ability = request.form["ability"].strip()
        time = request.form["time"].strip()
        user_id = session['id']

        if not name:
            errors.append("Campo nombre requerido")
        elif not satisfaction_level:
            errors.append("Campo nivel de satisfaccion requerido")
        elif not ability:
            errors.append("Campo habilidad requerido")
        elif not time:
            errors.append("Campo tiempo requerido")
        elif int(satisfaction_level) > 10 or int(satisfaction_level)<0:
            errors.append("Nivel de satisfaccion debe estar entre 0 y 10")

        if errors:
            return render_template('hobby.html',errors = errors)


        hobby = Hobby.query.filter_by(name=name,user_id = user_id ).first()
        if hobby:
            errors.append("Hobby ya existe")
            return render_template('hobby.html',errors = errors)
        else:
            hobby = Hobby(name, user_id, satisfaction_level, ability, time)
            db.session.add(hobby)
            db.session.commit()

    return render_template('hobby.html', msg="Hobby añadido")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True,host = '0.0.0.0')