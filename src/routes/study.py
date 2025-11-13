# En src/routes/study.py (DEBE QUEDAR ASÍ DE LIMPIO)

from flask import Blueprint, render_template, session
# Asegúrate de que solo importas lo necesario para esta página
from utils import login_required

study_bp = Blueprint(
    'study', __name__,
    template_folder='../templates',
    static_folder='../static'
)

@study_bp.route("/dashboard/study", methods=["GET"])
@login_required
def study():
    return render_template("study.html")

