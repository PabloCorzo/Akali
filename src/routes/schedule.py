from flask import Blueprint, render_template, request, flash, session, redirect, url_for, jsonify
from model import ScheduleItem, Activity, Task, Workout
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
            'id': item.id,
            'title': item.title,
            'start': item.start_time.isoformat(),
            'end': item.end_time.isoformat(),
            'extendedProps': {
                'item_type': item.item_type,
                'item_id': item.item_id
            }
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
            
            # Obtener tipo e ID del item (activity, task o custom)
            item_type = data.get('item_type', 'Custom')
            item_id = data.get('item_id', 0)
            
            new_item = ScheduleItem(
                user_id=user_id,
                title=data['title'],
                start_time=start_time,
                end_time=end_time,
                item_type=item_type,
                item_id=item_id
            )
            db.session.add(new_item)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Evento guardado'})

    
    activities = Activity.query.filter_by(user_id=user_id).all()
    tasks = Task.query.filter_by(_user_id=user_id).all()
    workouts = Workout.query.filter_by(user_id=user_id).all()

    return render_template('schedule.html', activities=activities, tasks=tasks, workouts=workouts)


@schedule_bp.route('/dashboard/schedule/events/<int:event_id>', methods=['PUT'])
@login_required
def update_schedule_item(event_id):
    """Actualiza un evento del calendario"""
    user_id = session['id']
    item = ScheduleItem.query.filter_by(_id=event_id, _user_id=user_id).first()
    
    if not item:
        return jsonify({'status': 'error', 'message': 'Evento no encontrado'}), 404
    
    data = request.get_json()
    
    try:
        if 'title' in data:
            item.title = data['title']
        if 'start' in data:
            # Manejar tanto formato con Z como sin Z
            start_str = data['start'].replace('Z', '+00:00') if 'Z' in data['start'] else data['start']
            item.start_time = datetime.fromisoformat(start_str)
        if 'end' in data:
            # Manejar tanto formato con Z como sin Z
            end_str = data['end'].replace('Z', '+00:00') if 'Z' in data['end'] else data['end']
            item.end_time = datetime.fromisoformat(end_str)
        
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Evento actualizado'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Error al actualizar: {str(e)}'}), 400


@schedule_bp.route('/dashboard/schedule/events/<int:event_id>', methods=['DELETE'])
@login_required
def delete_schedule_item(event_id):
    """Elimina un evento del calendario"""
    user_id = session['id']
    item = ScheduleItem.query.filter_by(_id=event_id, _user_id=user_id).first()
    
    if not item:
        return jsonify({'status': 'error', 'message': 'Evento no encontrado'}), 404
    
    db.session.delete(item)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Evento eliminado'})
