from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from model import Habit
from database import db
from utils import isLogged


habit_bp = Blueprint(
    'habits', __name__,
    template_folder='../templates',
    static_folder='../static'
)

@habit_bp.route("/dashboard/habitos", methods=["GET"])
def habitos():
    # Verificamos si el usuario está logueado
    if not isLogged():
        return redirect(url_for('auth.login'))

    # ID del usuario actual
    user_id = session['id']

    # Obtener los filtros del formulario de búsqueda
    q_name = (request.args.get("name") or "").strip()
    q_ability = (request.args.get("ability") or "").strip()

    # Saber si el usuario está buscando algo
    searched = any([q_name, q_ability])

    habits = []
    if searched:
        # Empezamos la consulta filtrando por usuario
        query = Habit.query.filter(Habit.user_id == user_id)
        if q_name:
            query = query.filter(Habit.name.ilike(f"%{q_name}%"))
        if q_ability:
            query = query.filter(Habit.ability.ilike(f"%{q_ability}%"))
        habits = query.order_by(Habit.id.desc()).all()

    # Renderizamos la plantilla y pasamos los resultados
    return render_template("habitos.html", habits=habits, searched=searched)



###################
@habit_bp.route("/dashboard/habitos/create", methods=["POST"])
def create_habit():
    # Verificamos si el usuario está logueado
    if not isLogged():
        return redirect(url_for('auth.login'))

    # Obtenemos el ID del usuario actual
    user_id = session['id']

    # Recogemos los datos del formulario
    name = (request.form.get("name") or "").strip()
    satisfaction_level = (request.form.get("satisfaction_level") or "").strip()
    ability = (request.form.get("ability") or "").strip()
    time = (request.form.get("time") or "").strip()

    # Validaciones básicas
    if not name:
        flash("El nombre del hábito es obligatorio", "habits_error")
        #flash("El nombre del hábito es obligatorio", "danger")
        return redirect(url_for("habits.habitos"))

    # Convertimos satisfaction_level y time a números si es posible
    satisfaction_level = int(satisfaction_level) if satisfaction_level else None
    time = float(time) if time else None

    # Verificamos si el hábito ya existe para el usuario actual
    existing = Habit.query.filter_by(name=name, user_id=user_id).first()
    if existing:
        #flash("Este hábito ya existe", "danger")
        flash("Este hábito ya existe", "habits_error")
        return redirect(url_for("habits.habitos"))

    # Creamos y guardamos el nuevo hábito
    habit = Habit(
        name=name,
        satisfaction_level=satisfaction_level,
        ability=ability,
        time=time,
        user_id=user_id
    )
    db.session.add(habit)
    db.session.commit()

    #flash("Hábito guardado correctamente", "success")
    flash("Hábito guardado correctamente", "habits_ok")
    return redirect(url_for("habits.habitos"))
