from flask import Blueprint, app, render_template, request, flash, session, redirect, url_for
from database import db
from utils import  isLogged, login_required

study_bp = Blueprint(
    'study', __name__,
    template_folder='../templates',
    static_folder='../static'
)

@study_bp.route("/dashboard/study", methods=["GET"])
@login_required
def study():
    return render_template("study.html")
