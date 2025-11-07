from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from model import Users, hashPassword
from database import db
from utils import isLogged

dashboard_bp = Blueprint(
    'dashboard', __name__,
    template_folder='../templates',  
    static_folder='../static'     
)

@dashboard_bp.route('/dashboard',methods = ['POST','GET'])
def dashboard():

    if not isLogged():
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')
