from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from model import Users, hashPassword
from database import db
from utils import isLogged, login_required

dashboard_bp = Blueprint(
    'dashboard', __name__,
    template_folder='../templates',
    static_folder='../static'
)


@dashboard_bp.route('/dashboard',methods = ['POST','GET'])
@login_required
def dashboard():

    return render_template('dashboard.html')
