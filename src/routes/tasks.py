from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from model import Task
from database import db
from utils import isLogged


tasks_bp = Blueprint(
    'tasks', __name__,
    template_folder='../templates',
    static_folder='../static'
)


@tasks_bp.route("/dashboard/tasks",methods = ['GET','POST'])
def tasks():
    if not isLogged():
        return redirect(url_for('auth.login'))

    uid = session['id']
    print(f"user id is : {uid}")
    task_list = Task.query.filter_by(_user_id = uid)
    print(task_list)
    return render_template('tasks.html', tasks = task_list)

@tasks_bp.route("/dashboard/tasks/create", methods = ['POST'])
def create_task():
    print("woopwoop")
    if not isLogged():
        return redirect(url_for('auth.login'))
    
    if request.form['task_name']:
        print(f"\n\nNAME IS {request.form['task_name']}\n\n")
        new_t = Task(request.form['task_name'],session['username'])
        if not Task.query.filter_by(name = request.form['task_name']).first():
            db.session.add(new_t)
            db.session.commit()
        else:
            pass
    return redirect(url_for('tasks.tasks'))

@tasks_bp.route("/dashboard/tasks/<int:task_id>/delete", methods=['POST'])
def delete_task(task_id):
    if not isLogged():
        return redirect(url_for('auth.login'))

    # Buscar la tarea del usuario actual
    tarea = Task.query.filter_by(_id=task_id, _user_id=session['id']).first()
    if tarea:
        db.session.delete(tarea)
        db.session.commit()
    return redirect(url_for('tasks.tasks'))

@tasks_bp.route("/dashboard/tasks/<int:task_id>/toggle", methods=['POST'])
def toggle_task(task_id):
    if not isLogged():
        return redirect(url_for('auth.login'))

    t = Task.query.filter_by(_id=task_id, _user_id=session['id']).first_or_404()
    t.completed = not bool(t.completed)
    db.session.commit()
    return redirect(url_for('tasks.tasks'))

