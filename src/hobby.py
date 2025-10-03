from flask import Flask,render_template,request,flash, session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from app import Users

def create_hobby(app : Flask, request,session,db):
    errors = []
    if not session.get('loggedin'):
        return redirect(url_for('login'))

    user_id = session['id']
    if not user_id:
        return redirect(url_for('login'))

    if request.method == "POST":
        name = request.form["name"].strip()
        satisfaction_level = request.form["satisfaction_level"].strip()
        hability = request.form["hability"].strip()
        time = request.form["time"].strip()

        if not name:
            errors.append("Campo nombre requerido")
        elif not satisfaction_level:
            errors.append("Campo nivel de satisfaccion requerido")
        elif not hability:
            errors.append("Campo habilidad requerido")
        elif not time:
            errors.append("Campo tiempo requerido")
        elif int(satisfaction_level) > 10 or int(satisfaction_level)<0:
            errors.append("Nivel de satisfaccion debe estar entre 0 y 10")

        if errors:
            return render_template('hobby.html',errors = errors)

        hobby = db.fetchQuery(query=f"SELECT * FROM hobbies WHERE user_id = {user_id} AND name = '{name}'")
        if hobby:
            errors.append("Hobby ya existe")
            return render_template('hobby.html',errors = errors)
        db.fetchQuery(query= f"iNSERT INTO hobbies (user_id,name,satisfaction_level,hability,time) VALUES ({user_id},'{name}','{satisfaction_level}','{hability}','{time}')")
    return render_template('hobby.html', msg="Hobby añadido")
