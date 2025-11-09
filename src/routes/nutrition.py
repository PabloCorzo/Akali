from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from model import NutritionEntry
from datetime import datetime
from database import db
from utils import  isLogged, login_required

nutrition_bp = Blueprint(
    'nutrition', __name__,
    template_folder='../templates',
    static_folder='../static'
)

# -------------------- NUEVAS RUTAS: NUTRICIÓN --------------------
@nutrition_bp.route("/fitness/nutrition", methods=["GET"])
@login_required
def nutrition_list():
    entries = NutritionEntry.query.filter_by(user_id=session['id']).order_by(NutritionEntry.date.desc()).all()
    resume = {}
    for e in entries:
        k = e.date.strftime("%Y-%m-%d")
        resume.setdefault(k, {"kcal": 0, "p": 0, "c": 0, "g": 0})
        resume[k]["kcal"] += e.calories
        resume[k]["p"] += e.protein_g
        resume[k]["c"] += e.carbs_g
        resume[k]["g"] += e.fat_g
    return render_template("nutrition.html", entries=entries, resume=resume)


@nutrition_bp.route("/fitness/nutrition/new", methods=["GET", "POST"])
@login_required
def nutrition_new():
    if request.method == "POST":
        e = NutritionEntry(
            user_id=session['id'],
            date=datetime.strptime(request.form.get("date"), "%Y-%m-%d") if request.form.get("date") else datetime.utcnow(),
            meal_type=request.form.get("meal_type"),
            food=request.form["food"],
            calories=int(request.form.get("calories") or 0),
            protein_g=float(request.form.get("protein_g") or 0),
            carbs_g=float(request.form.get("carbs_g") or 0),
            fat_g=float(request.form.get("fat_g") or 0),
            notes=request.form.get("notes")
        )
        db.session.add(e); db.session.commit()
        flash("Registro nutricional añadido", "success")
        return redirect(url_for("nutrition.nutrition_list"))

    return render_template("nutrition_form.html")
