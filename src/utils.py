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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not isLogged():
            flash("Debes iniciar sesión para ver esta página.", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function