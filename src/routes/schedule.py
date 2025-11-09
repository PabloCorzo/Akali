from flask import Blueprint, render_template, request, flash, session, redirect, url_for, jsonify
from model import ScheduleItem, Activity, Task
from datetime import datetime
from database import db
from utils import isLogged, login_required

schedule_bp = Blueprint('schedule', __name__,
    template_folder='../templates', static_folder='../static')


@schedule_bp.route('/dashboard/schedule/events')
def get_schedule_events():
    """
    Esta nueva ruta es como un 'menú de eventos' para el calendario.
    El calendario le pedirá los eventos a esta URL y los mostraremos en formato JSON.
    """
    if not isLogged():
        return jsonify([]) # Devuelve una lista vacía si el usuario no está logueado

    user_id = session['id']
    schedule_items = ScheduleItem.query.filter_by(_user_id=user_id).all()

    events = []
    for item in schedule_items:
        events.append({
            'title': item.title,
            'start': item.start_time.isoformat(),
            'end': item.end_time.isoformat()
        })
    return jsonify(events)


@schedule_bp.route("/dashboard/schedule",methods = ['GET','POST'])
@login_required
def create_schedule_item():
    """
    Modificamos esta ruta para que pueda recibir peticiones tanto
    del formulario antiguo como del nuevo calendario interactivo.
    """
    user_id = session['id']

    if request.method == 'POST':
        # Esta nueva sección es para cuando JavaScript envía un nuevo evento.
        if request.is_json:
            data = request.get_json()
            start_time = datetime.fromisoformat(data['start'])
            end_time = datetime.fromisoformat(data['end'])
            new_item = ScheduleItem(
                user_id=user_id,
                title=data['title'],
                start_time=start_time,
                end_time=end_time,
                item_type='Custom', # Asignamos un tipo por defecto
                item_id=0           # Asignamos un ID por defecto
            )
            db.session.add(new_item)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Evento guardado'})

    
    activities = Activity.query.filter_by(user_id=user_id).all()
    tasks = Task.query.filter_by(_user_id=user_id).all()

    return render_template('schedule.html', activities=activities, tasks=tasks)
