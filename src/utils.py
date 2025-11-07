from flask import session
from model import Users

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