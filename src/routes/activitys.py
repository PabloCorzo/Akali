from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from database import db
from utils import  isLogged, login_required
from model import Activity
from bad_words import BAD_WORDS


def contains_bad_word(text):
    text = text.lower()
    return any(bad in text for bad in BAD_WORDS)

activity_bp = Blueprint(
    'activity', __name__,
    template_folder='../templates',
    static_folder='../static'
)


@activity_bp.route("/dashboard/activity", methods=["POST", "GET"])
@login_required
def create_Activity():

    errors = []
    user_id = session['id']
    
    name = request.args.get("b_name")

    if name:
        activities = Activity.query.filter(
            Activity.user_id == user_id,
            Activity.name.ilike(f'%{name}%')
        ).all()
        if not activities:
            flash("No se encontraron actividades con ese nombre.", "warning")
    else:
        activities = Activity.query.filter_by(user_id=user_id).all()

    if request.method == "POST":
        name = request.form["name"].strip()
        satisfaction_level = request.form["satisfaction_level"].strip()
        ability = request.form["ability"].strip()
        time = request.form["time"].strip()

        # --- AQUI VA EL BLOQUE PARA LA MASCOTA ---
        is_bad = contains_bad_word(name)
        session["activity_bad"] = is_bad
        # -------------------------

        if not name:
            errors.append("Campo nombre requerido")
        elif not satisfaction_level:
            errors.append("Campo nivel de satisfaccion requerido")
        elif not ability:
            errors.append("Campo habilidad requerido")
        elif  int(time) > 168 or int(time) < 0:
            errors.append("El tiempo tiene que ser 168 como maximo")
        elif not time:
            errors.append("Campo tiempo requerido")
        elif int(satisfaction_level) > 10 or int(satisfaction_level) < 0:
            errors.append("Nivel de satisfaccion debe estar entre 0 y 10")

        if errors:
            return render_template('activity.html', errors=errors, Activity=activities)

        existing_activity = Activity.query.filter_by(name=name, user_id=user_id).first()
        if existing_activity:
            flash("La actividad ya existe", "danger")
            errors.append("La actividad ya existe")
            return render_template('activity.html', errors=errors, Activity=activities)
        else:
            activity = Activity(name, user_id, satisfaction_level, ability, time)
            activity = Activity(name, user_id, satisfaction_level, ability, time)
            db.session.add(activity)
            db.session.commit()

            #Recargar actividades después de crear una nueva
            activities = activity.query.filter_by(user_id=user_id).all()


    return render_template('activity.html',
                           Activity=activities,
                           errors=errors,
                           activity_bad=session.get("activity_bad", False))
