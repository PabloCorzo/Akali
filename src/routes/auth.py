from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from model import Users, hashPassword
from database import db
from utils import checkPassword
from routes.coins_manager import CoinsManager

#Crear un blueprint para que funciones
auth_bp = Blueprint(
    'auth', __name__,
    template_folder='../templates',  
    static_folder='../static'     
)


@auth_bp.route('/', methods=['POST', 'GET'])
def home():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
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

            # Intentar reclamar monedas diarias
            success, message = CoinsManager.claim_daily_coins(user._id, 10)
            if success:
                flash(message, "success")
            else:
                flash(message, "info")

            session['show_coins_message'] = True
            session["game"] = None
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash("Usuario o Contraseña Incorrecto ❌", "danger")
            return render_template("login.html")
    else:
        return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('auth.login'))
    return render_template('signup.html')


@auth_bp.route('/logout', methods=['POST', 'GET'])
def logout():
    session['id'] = None
    session['username'] = None
    return redirect(url_for('auth.login'))
