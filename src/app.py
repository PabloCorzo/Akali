from flask import Flask, render_template, request, flash, session, redirect, url_for
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

app.config["SESSION_PERMANENT"] = False

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


def isLogged() -> bool:

    #Lanza error si intena acceder a una variable de sesion que no existe
    try:
        has_user = session['username'] is not None
        has_id = session['id'] is not None
        return  has_user and has_id
    except:
        return False


class Users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(32), unique=True, nullable=False)
    email = db.Column('email', db.String(32), unique=True, nullable=True)
    password = db.Column('password', db.String(32), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.hashPassword(password)

def hashPassword(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def checkPassword(username, password):
    return Users.query.filter_by(username=username, password=password).first()


class Hobby(db.Model):
    _hobby_id = db.Column('hobby_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), unique=False, nullable=False)
    user_id = db.Column('user_id', db.Integer, unique=False, nullable=True)
    satisfaction_level = db.Column('satisfaction_level', db.Integer, nullable=True)
    ability = db.Column('ability', db.String(100), nullable=True)
    time = db.Column('time', db.Time, nullable=True)

    def __init__(self, name, user_id, satisfaction_level, ability, time):
        self.name = name
        self.user_id = user_id
        self.satisfaction_level = satisfaction_level
        self.ability = ability
        self.time = time


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    director = db.Column(db.String(255), nullable=True)
    actors = db.Column(db.String(500), nullable=True)
    synopsis = db.Column(db.Text, nullable=True)

    def __init__(self, title, director=None, actors=None, synopsis=None):
        self.title = title
        self.director = director
        self.actors = actors
        self.synopsis = synopsis


@app.route('/', methods=['POST', 'GET'])
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(f"Login iniciado con metodo: {request.method}")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not password:
            password = "inv"
        if not username:
            username = "inv"
        # email = request.form['email']
        # print(f'username {username} password {password},{}')
        user = Users.query.filter_by(username=username).first()
        passw = hashPassword(password = password)
        if checkPassword(username, passw):
            session['username'] = user.username
            # session['email'] = user.email
            session['id'] = user._id
            return redirect(url_for('dashboard'))
        else:
            return render_template("login.html", error="Invalid user")
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if email is None:
            email = ""
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('index.html', error='user already registered')
        else:
            user = Users(username=username, password=password, email=email)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session['id'] = None
    session['username'] = None
    return redirect(url_for('/'))

@app.route('/dashboard',methods = ['POST','GET'])
def dashboard():

    if not isLogged():
        return redirect(url_for('login'))
    return render_template('dashboard.html')



@app.route("/dashboard/hobby", methods=["POST", "GET"])
def create_hobby():

    errors = []
    if not isLogged():
        return redirect(url_for('login'))

    user_id = session['id']

    name = request.args.get("b_name")

    if name:
        hobbies = Hobby.query.filter(
            Hobby.user_id == user_id,
            Hobby.name.ilike(f'%{name}%')
        ).all()
        if not hobbies:
            flash("No se encontraron hobbies con ese nombre.", "warning")
    else:
        hobbies = Hobby.query.filter_by(user_id=user_id).all()

    if request.method == "POST":
        name = request.form["name"].strip()
        satisfaction_level = request.form["satisfaction_level"].strip()
        ability = request.form["ability"].strip()
        time = request.form["time"].strip()

        if not name:
            errors.append("Campo nombre requerido")
        elif not satisfaction_level:
            errors.append("Campo nivel de satisfaccion requerido")
        elif not ability:
            errors.append("Campo habilidad requerido")
        elif not time:
            errors.append("Campo tiempo requerido")
        elif int(satisfaction_level) > 10 or int(satisfaction_level) < 0:
            errors.append("Nivel de satisfaccion debe estar entre 0 y 10")

        if errors:
            return render_template('hobby.html', errors=errors)

        hobby = Hobby.query.filter_by(name=name, user_id=user_id).first()
        if hobby:
            errors.append("Hobby ya existe")
            return render_template('hobby.html', errors=errors)
        else:
            hobby = Hobby(name, user_id, satisfaction_level, ability, time)
            db.session.add(hobby)
            db.session.commit()

    return render_template('hobby.html', hobby=hobbies)


@app.route("/dashboard/movies", methods=["GET"])
def movies():

    if not isLogged():
        return redirect(url_for('login'))

    # parámetros de búsqueda
    q_title = (request.args.get("title") or "").strip()
    q_director = (request.args.get("director") or "").strip()
    q_actor = (request.args.get("actor") or "").strip()

    query = Movie.query
    if q_title:
        query = query.filter(Movie.title.ilike(f"%{q_title}%"))
    if q_director:
        query = query.filter(Movie.director.ilike(f"%{q_director}%"))
    if q_actor:
        # búsqueda simple de substring dentro del campo actors
        query = query.filter(Movie.actors.ilike(f"%{q_actor}%"))

    results = query.order_by(Movie.id.desc()).all()
    return render_template("movies.html", movies=results)


@app.route("/dashboard/movies/create", methods=["POST"])
def create_movie():

    if not isLogged():
        return redirect(url_for('login'))

    title = (request.form.get("title") or "").strip()
    director = (request.form.get("director") or "").strip() or None
    actors = (request.form.get("actors") or "").strip() or None
    synopsis = (request.form.get("synopsis") or "").strip() or None

    if not title:
        flash("El título es obligatorio", "error")
        return redirect(url_for("movies"))

    m = Movie(title=title, director=director, actors=actors, synopsis=synopsis)
    db.session.add(m)
    db.session.commit()
    flash("Película guardada", "success")
    return redirect(url_for("movies"))



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True,host = '0.0.0.0')

