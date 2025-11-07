from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from model import Workout, Exercise
from datetime import datetime
from database import db
from utils import  isLogged

workout_bp = Blueprint(
    'workout', __name__,
    template_folder='../templates',
    static_folder='../static'
)   

# -------------------- NUEVAS RUTAS: ENTRENAMIENTOS --------------------
@workout_bp.route("/fitness/workouts", methods=["GET"])
def workouts_list():
    if not isLogged():
        return redirect(url_for('auth.login'))
    ws = Workout.query.filter_by(user_id=session['id']).order_by(Workout.date.desc()).all()
    return render_template("workouts.html", workouts=ws)


@workout_bp.route("/fitness/workouts/new", methods=["GET", "POST"])
def workouts_new():
    if not isLogged():
        return redirect(url_for('auth.login'))
    if request.method == "POST":
        w = Workout(
            user_id=session['id'],
            title=(request.form.get("title") or "Entrenamiento").strip(),
            date=datetime.strptime(request.form.get("date"), "%Y-%m-%d") if request.form.get("date") else datetime.utcnow(),
            duration_min=int(request.form.get("duration_min") or 0),
            notes=request.form.get("notes")
        )
        db.session.add(w); db.session.flush()

        names  = request.form.getlist("ex_name[]")
        kinds  = request.form.getlist("ex_kind[]")
        sets_  = request.form.getlist("ex_sets[]")
        reps   = request.form.getlist("ex_reps[]")
        weight = request.form.getlist("ex_weight[]")
        time_  = request.form.getlist("ex_time[]")
        dist   = request.form.getlist("ex_distance[]")

        for i in range(len(names)):
            if not names[i].strip():
                continue
            db.session.add(Exercise(
                workout_id=w.id, name=names[i], kind=kinds[i] or None,
                sets=int(sets_[i] or 0) if sets_ else None,
                reps=int(reps[i] or 0) if reps else None,
                weight_kg=float(weight[i] or 0) if weight else None,
                time_sec=int(time_[i] or 0) if time_ else None,
                distance_km=float(dist[i] or 0) if dist else None
            ))
        db.session.commit()
        flash("Entrenamiento guardado", "success")
        return redirect(url_for("workout.workouts_list"))

    return render_template("workout_form.html")
