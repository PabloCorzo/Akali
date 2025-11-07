from flask import Blueprint, app, render_template, request, flash, session, redirect, url_for
from database import db
from utils import  isLogged

study_bp = Blueprint(
    'study', __name__,
    template_folder='../templates',
    static_folder='../static'
)

@study_bp.route("/dashboard/study", methods=["GET"])
def study():
    if not isLogged():
        return redirect(url_for('auth.login'))
    return render_template("study.html")
