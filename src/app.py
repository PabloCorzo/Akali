from flask import Flask,render_template,request,flash, session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
# import src.db_repository as db
import re
import hashlib



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
            return redirect(url_for('dashboard'))
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
    if not session.get('loggedin'):
        return redirect(url_for('login'))

    user_id = session['id']
    if not user_id:
        return redirect(url_for('login'))

    if request.method == "POST":
        name = request.form["name"].strip()
        satisfaction_level = request.form["satisfaction_level"].strip()
        hability = request.form["hability"].strip()
        time = request.form["time"].strip()

        if not name:
            errors.append("Campo nombre requerido")
        elif not satisfaction_level:
            errors.append("Campo nivel de satisfaccion requerido")
        elif not hability:
            errors.append("Campo habilidad requerido")
        elif not time:
            errors.append("Campo tiempo requerido")
        elif int(satisfaction_level) > 10 or int(satisfaction_level)<0:
            errors.append("Nivel de satisfaccion debe estar entre 0 y 10")

        if errors:
            return render_template('hobby.html',errors = errors)

        hobby = db.fetchQuery(query=f"SELECT * FROM hobbies WHERE user_id = {user_id} AND name = '{name}'")
        if hobby:
            errors.append("Hobby ya existe")
            return render_template('hobby.html',errors = errors)
        db.fetchQuery(query= f"iNSERT INTO hobbies (user_id,name,satisfaction_level,hability,time) VALUES ({user_id},'{name}','{satisfaction_level}','{hability}','{time}')")
    return render_template('hobby.html', msg="Hobby añadido")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True,host = '0.0.0.0')