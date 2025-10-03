from flask import Flask,render_template,request,flash, session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
# import src.db_repository as db
import loginscripts,hobby
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
    username = db.Column(db.String(32),unique = True,nullable = False)
    mail = db.Column(db.String(32),unique = True,nullable = True)
    password = db.Column(db.String(32),nullable = False)

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = self.hashPassword(password)

    def hashPassword(self,password : str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    def checkPassword(self):
        return Users.query.filter_by(username = self.username, password = self.password)

@app.route('/',methods = ['POST','GET'])
def home():
    return redirect(url_for('register'))

@app.route('/login', methods = ['GET','POST'])
def login():
    return loginscripts.login(app = app, request = request, session = session)

@app.route('/register', methods = ['GET','POST'])
def register():
    return loginscripts.register(app = app, request = request,db = db)

@app.route('/logout', methods = ['POST','GET'])
def logout():
    return loginscripts.logout(app = app, request = request, session = session)

@app.route('/dashboard',methods = ['POST','GET'])
def dashboard():
    return f"<h1>Dashboard</h1>"

@app.route("/hobby",methods = ["POST","GET"])
def create_hobby():
    return hobby.create_hobby(app = app, request = request, session = session, db = db)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True,host = '0.0.0.0')