from flask import Blueprint, render_template, request, flash, session, redirect, url_for, jsonify
from model import Workout, Exercise
from datetime import datetime
from database import db
from utils import  isLogged, login_required

workout_bp = Blueprint(
    'workout', __name__,
    template_folder='../templates',
    static_folder='../static'
)   

# -------------------- NUEVAS RUTAS: ENTRENAMIENTOS --------------------
@workout_bp.route("/fitness/workouts", methods=["GET"])
@login_required
def workouts_list():
    ws = Workout.query.filter_by(user_id=session['id']).order_by(Workout.date.desc()).all()
    return render_template("workouts.html", workouts=ws)


@workout_bp.route("/fitness/workouts/new", methods=["GET", "POST"])
@login_required
def workouts_new():
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


@workout_bp.route("/fitness/workouts/<int:workout_id>/update-duration", methods=["POST"])
@login_required
def update_workout_duration(workout_id):
    """Actualiza la duración de un entrenamiento"""
    workout = Workout.query.filter_by(id=workout_id, user_id=session['id']).first()
    
    if not workout:
        return jsonify({'status': 'error', 'message': 'Entrenamiento no encontrado'}), 404
    
    data = request.get_json()
    new_duration = data.get('duration')
    
    if new_duration is None or new_duration <= 0:
        return jsonify({'status': 'error', 'message': 'Duración inválida'}), 400
    
    old_duration = workout.duration_min
    workout.duration_min = int(new_duration)
    db.session.commit()
    
    return jsonify({
        'status': 'success', 
        'message': 'Duración actualizada',
        'old_duration': old_duration,
        'new_duration': workout.duration_min
    })
