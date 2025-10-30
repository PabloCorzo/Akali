from flask import Flask, jsonify, render_template, request, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import sys
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import re
import hashlib
from datetime import datetime, time


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

def hashPassword(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def checkPassword(username, password):
    return Users.query.filter_by(username=username, password=password).first()

class Users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(32), unique=True, nullable=False)
    email = db.Column('email', db.String(32), unique=True, nullable=True)
    password = db.Column('password', db.String(64), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = hashPassword(password)

class Task(db.Model):
    _id = db.Column('task_id', db.Integer, primary_key=True,unique = True)
    name = db.Column('name', db.String(32), unique=False, nullable=False)
    completed = db.Column('completed', db.Boolean, unique=False, nullable=True)
    _user_id = db.Column('user_id',db.Integer, unique = False, nullable = False)
    def __init__(self,name, user):
        self.name = name
        self._user_id = Users.query.filter_by(username = user).first()._id
        self.completed = 0
        
class ScheduleItem(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    _user_id = db.Column('user_id',db.Integer, unique = False, nullable = False)
    title = db.Column('title', db.String(100), unique=False, nullable=False)
    start_time = db.Column('start_time', db.DateTime, unique=False, nullable=False)
    end_time = db.Column('end_time', db.DateTime, unique=False, nullable=False)
    item_type = db.Column('item_type', db.String(50), unique=False, nullable=False)
    item_id = db.Column('item_id', db.Integer, unique=False, nullable=False)
    
    def __init__(self, user_id, title, start_time, end_time, item_type, item_id):
        self._user_id = user_id
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.item_type = item_type
        self.item_id = item_id

class Hobby(db.Model):
    _hobby_id = db.Column('hobby_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), unique=False, nullable=False)
    user_id = db.Column('user_id', db.Integer, unique=False, nullable=True)
    satisfaction_level = db.Column('satisfaction_level', db.Integer, nullable=True)
    ability = db.Column('ability', db.String(100), nullable=True)
    time = db.Column('time', db.Float, nullable=True)

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
    ###########
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, director=None, actors=None, synopsis=None, user_id=None):
        self.title = title
        self.director = director
        self.actors = actors
        self.synopsis = synopsis
        ##############
        self.user_id = user_id

##########################
class Habit(db.Model):
    __tablename__ = 'habits'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    satisfaction_level = db.Column(db.Integer, nullable=True)
    ability = db.Column(db.String(100), nullable=True)
    time = db.Column(db.Float, nullable=True)
    ###########
    user_id = db.Column('user_id', db.Integer, unique=False, nullable=True)

    def __init__(self, name, satisfaction_level=None, ability=None, time=None, user_id=None):
        self.name = name
        self.satisfaction_level = satisfaction_level
        self.ability = ability
        self.time = time
        ##############
        self.user_id = user_id

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)

    def __init__(self, title):
        self.title = title




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
        # print(f'username {username} password {password},{{}}')
        user = Users.query.filter_by(username=username).first()
        passw = hashPassword(password = password)
        if checkPassword(username, passw):
            session['username'] = user.username
            # session['email'] = user.email
            session['id'] = user._id
            return redirect(url_for('dashboard'))
        else:
            flash("Usuario o Contraseña Incorrecto ❌", "danger")
            return render_template("login.html")
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        def mail_exists():
            return Users.query.filter_by(email=email).first()
        
        
        user = Users.query.filter_by(username=username).first()
        
        if user:
            flash('Usuario ya existe','danger')
            return render_template('signup.html')

        if mail_exists():
            flash('Correo ya registrado','danger')
            return render_template('signup.html')
        else:
            user = Users(username=username, password=password, email=email)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session['id'] = None
    session['username'] = None
    return redirect(url_for('login'))

@app.route('/dashboard',methods = ['POST','GET'])
def dashboard():

    if not isLogged():
        return redirect(url_for('login'))
    return render_template('dashboard.html')
    
    user_id = session['id']
    # Obtenemos todos los items del horario para el usuario.
    # Idealmente, aquí filtrarías por el día actual, pero para empezar mostraremos todos.
    schedule_items = ScheduleItem.query.filter_by(_user_id=user_id).order_by(ScheduleItem.start_time).all()
    return render_template('dashboard.html', schedule=schedule_items)



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
        elif  int(time) > 168 or int(time) < 0:
            errors.append("El tiempo tiene que ser 168 como maximo")
        elif not time:
            errors.append("Campo tiempo requerido")
        elif int(satisfaction_level) > 10 or int(satisfaction_level) < 0:
            errors.append("Nivel de satisfaccion debe estar entre 0 y 10")

        if errors:
            return render_template('hobby.html', errors=errors)

        hobby = Hobby.query.filter_by(name=name, user_id=user_id).first()
        if hobby:
            flash("El Hobby ya existe", "danger")
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

    q_title    = (request.args.get("title") or "").strip()
    q_director = (request.args.get("director") or "").strip()
    q_actor    = (request.args.get("actor") or "").strip()

    searched = any([q_title, q_director, q_actor])

    movies = []
    if searched:
        query = Movie.query.filter(Movie.user_id == session['id'])
        if q_title:
            query = query.filter(Movie.title.ilike(f"%{q_title}%"))
        if q_director:
            query = query.filter(Movie.director.ilike(f"%{q_director}%"))
        if q_actor:
            query = query.filter(Movie.actors.ilike(f"%{q_actor}%"))
        movies = query.order_by(Movie.id.desc()).all()

    return render_template("movies.html", movies=movies, searched=searched)

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

    ###########
    owner_id = session['id']
    m = Movie(title=title, director=director, actors=actors, synopsis=synopsis,user_id=owner_id)
    db.session.add(m)
    db.session.commit()
    flash("Película guardada", "success")
    return redirect(url_for("movies"))

@app.route("/dashboard/tasks",methods = ['GET','POST'])
def tasks():
    if not isLogged():
        return redirect(url_for('login'))

    uid = session['id']
    print(f"user id is : {uid}")
    task_list = Task.query.filter_by(_user_id = uid)
    print(task_list)
    return render_template('tasks.html', tasks = task_list)

@app.route("/dashboard/tasks/create", methods = ['POST'])
def create_task():
    print("woopwoop")
    if not isLogged():
        return redirect(url_for('login'))
    
    if request.form['task_name']:
        print(f"\n\nNAME IS {request.form['task_name']}\n\n")
        new_t = Task(request.form['task_name'],session['username'])
        if not Task.query.filter_by(name = request.form['task_name']).first():
            db.session.add(new_t)
            db.session.commit()
        else:
            pass
    return redirect(url_for('tasks'))

@app.route("/dashboard/tasks/<int:task_id>/delete", methods=['POST'])
def delete_task(task_id):
    if not isLogged():
        return redirect(url_for('login'))

    # Buscar la tarea del usuario actual
    tarea = Task.query.filter_by(_id=task_id, _user_id=session['id']).first()
    if tarea:
        db.session.delete(tarea)
        db.session.commit()
    return redirect(url_for('tasks'))

@app.route("/dashboard/tasks/<int:task_id>/toggle", methods=['POST'])
def toggle_task(task_id):
    if not isLogged():
        return redirect(url_for('login'))

    t = Task.query.filter_by(_id=task_id, _user_id=session['id']).first_or_404()
    t.completed = not bool(t.completed)
    db.session.commit()
    return redirect(url_for('tasks'))



#########
@app.route("/dashboard/habitos", methods=["GET"])
def habitos():
    # Verificamos si el usuario está logueado
    if not isLogged():
        return redirect(url_for('login'))

    # ID del usuario actual
    user_id = session['id']

    # Obtener los filtros del formulario de búsqueda
    q_name = (request.args.get("name") or "").strip()
    q_ability = (request.args.get("ability") or "").strip()

    # Saber si el usuario está buscando algo
    searched = any([q_name, q_ability])

    habits = []
    if searched:
        # Empezamos la consulta filtrando por usuario
        query = Habit.query.filter(Habit.user_id == user_id)
        if q_name:
            query = query.filter(Habit.name.ilike(f"%{q_name}%"))
        if q_ability:
            query = query.filter(Habit.ability.ilike(f"%{q_ability}%"))
        habits = query.order_by(Habit.id.desc()).all()

    # Renderizamos la plantilla y pasamos los resultados
    return render_template("habitos.html", habits=habits, searched=searched)



###################
@app.route("/dashboard/habitos/create", methods=["POST"])
def create_habit():
    # Verificamos si el usuario está logueado
    if not isLogged():
        return redirect(url_for('login'))

    # Obtenemos el ID del usuario actual
    user_id = session['id']

    # Recogemos los datos del formulario
    name = (request.form.get("name") or "").strip()
    satisfaction_level = (request.form.get("satisfaction_level") or "").strip()
    ability = (request.form.get("ability") or "").strip()
    time = (request.form.get("time") or "").strip()

    # Validaciones básicas
    if not name:
        flash("El nombre del hábito es obligatorio", "habits_error")
        #flash("El nombre del hábito es obligatorio", "danger")
        return redirect(url_for("habitos"))

    # Convertimos satisfaction_level y time a números si es posible
    satisfaction_level = int(satisfaction_level) if satisfaction_level else None
    time = float(time) if time else None

    # Verificamos si el hábito ya existe para el usuario actual
    existing = Habit.query.filter_by(name=name, user_id=user_id).first()
    if existing:
        #flash("Este hábito ya existe", "danger")
        flash("Este hábito ya existe", "habits_error")
        return redirect(url_for("habitos"))

    # Creamos y guardamos el nuevo hábito
    habit = Habit(
        name=name,
        satisfaction_level=satisfaction_level,
        ability=ability,
        time=time,
        user_id=user_id
    )
    db.session.add(habit)
    db.session.commit()

    #flash("Hábito guardado correctamente", "success")
    flash("Hábito guardado correctamente", "habits_ok")
    return redirect(url_for("habitos"))


@app.route('/dashboard/schedule/events')
def get_schedule_events():
    """
    Esta nueva ruta es como un 'menú de eventos' para el calendario.
    El calendario le pedirá los eventos a esta URL y los mostraremos en formato JSON.
    """
    if not isLogged():
        return jsonify([]) # Devuelve una lista vacía si el usuario no está logueado

    user_id = session['id']
    schedule_items = ScheduleItem.query.filter_by(_user_id=user_id).all()

    events = []
    for item in schedule_items:
        events.append({
            'title': item.title,
            'start': item.start_time.isoformat(),
            'end': item.end_time.isoformat()
        })
    return jsonify(events)


@app.route("/dashboard/schedule",methods = ['GET','POST'])
def create_schedule_item():
    """
    Modificamos esta ruta para que pueda recibir peticiones tanto
    del formulario antiguo como del nuevo calendario interactivo.
    """
    if not isLogged():
        return redirect(url_for('login'))

    user_id = session['id']

    if request.method == 'POST':
        # Esta nueva sección es para cuando JavaScript envía un nuevo evento.
        if request.is_json:
            data = request.get_json()
            start_time = datetime.fromisoformat(data['start'])
            end_time = datetime.fromisoformat(data['end'])
            new_item = ScheduleItem(
                user_id=user_id,
                title=data['title'],
                start_time=start_time,
                end_time=end_time,
                item_type='Custom', # Asignamos un tipo por defecto
                item_id=0           # Asignamos un ID por defecto
            )
            db.session.add(new_item)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Evento guardado'})

    
    hobbies = Hobby.query.filter_by(user_id=user_id).all()
    tasks = Task.query.filter_by(_user_id=user_id).all()
    habits = Habit.query.filter_by(user_id=user_id).all()

    return render_template('schedule.html', hobbies=hobbies, tasks=tasks, habits=habits)


@app.route("/dashboard/games", methods=["GET"])
def games():
    if not isLogged():
        return redirect(url_for('login'))

    q_title    = (request.args.get("title") or "").strip()

    searched = any([q_title])

    games = []
    if searched:
        query = Game.query.filter(Game.user_id == session['id'])
        if q_title:
            query = query.filter(Game.title.ilike(f"%{q_title}%"))
        games = query.order_by(Game.id.desc()).all()

    return render_template("games.html", games=games, searched=searched)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True,host = '0.0.0.0')