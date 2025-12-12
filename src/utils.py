from flask import session, url_for,flash, redirect
from model import Users
from functools import wraps

def isLogged() -> bool:
    """Verifica si el usuario está logueado"""
    try:
        has_user = session['username'] is not None
        has_id = session['id'] is not None
        return has_user and has_id
    except:
        return False

def checkPassword(username, password):
    """Verifica si la contraseña es correcta para el usuario dado"""
    return Users.query.filter_by(username=username, password=password).first()

def inject_user_coins():
    """Hace que las monedas del usuario estén disponibles en todos los templates"""
    if 'id' in session:
        # user = Users.query.filter_by(_id = session['id']).first()
        user = Users.query.get(session['id'])
        if user:
            return {'user_coins': user.coins, 'user_name': user.username}
    return {'user_coins': 0, 'user_name': None}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not isLogged():
            flash("Debes iniciar sesión para ver esta página.", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function