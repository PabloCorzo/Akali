from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from model import Users, hashPassword
from database import db
from utils import  isLogged
from model import Hobby

hobbies_bp = Blueprint(
    'hobbies', __name__,
    template_folder='../templates',
    static_folder='../static'
)


@hobbies_bp.route("/dashboard/hobbies", methods=["POST", "GET"])
def create_hobby():

    errors = []
    if not isLogged():
        return redirect(url_for('auth.login'))
    
    user_id = session['id']

    name = request.args.get("b_name")

    if name:
        hobbies = Hobby.query.filter(
            Hobby.user_id == user_id,
            Hobby.name.ilike(f'%{name}%')
        ).all()
        if not hobbies:
            flash("No se encontraron hobbies con ese nombre.", "warning")
    else:
        hobbies = Hobby.query.filter_by(user_id=user_id).all()

    if request.method == "POST":
        name = request.form["name"].strip()
        satisfaction_level = request.form["satisfaction_level"].strip()
        ability = request.form["ability"].strip()
        time = request.form["time"].strip()

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
            return render_template('hobby.html', errors=errors)

        hobby = Hobby.query.filter_by(name=name, user_id=user_id).first()
        if hobby:
            flash("El Hobby ya existe", "danger")
            errors.append("Hobby ya existe")
            return render_template('hobby.html', errors=errors)
        else:
            hobby = Hobby(name, user_id, satisfaction_level, ability, time)
            db.session.add(hobby)
            db.session.commit()

    return render_template('hobby.html', hobby=hobbies)
