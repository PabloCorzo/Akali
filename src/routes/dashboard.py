from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from model import Users, Task, ScheduleItem
from database import db
from utils import isLogged, login_required
from datetime import datetime, date, timedelta

dashboard_bp = Blueprint(
    'dashboard', __name__,
    template_folder='../templates',
    static_folder='../static'
)


@dashboard_bp.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    user_id = session['id']
    
    # Obtener las 5 tareas pendientes más recientes
    tasks = Task.query.filter_by(
        _user_id=user_id,
        completed=False
    ).order_by(Task._id.desc()).limit(5).all()
    
    # Obtener eventos de hoy
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    events = ScheduleItem.query.filter(
        ScheduleItem._user_id == user_id,
        ScheduleItem.start_time >= today_start,
        ScheduleItem.start_time <= today_end
    ).order_by(ScheduleItem.start_time).all()
    
    # Obtener eventos de los próximos 7 días para el mini calendario
    week_end = today_start + timedelta(days=7)
    week_events = ScheduleItem.query.filter(
        ScheduleItem._user_id == user_id,
        ScheduleItem.start_time >= today_start,
        ScheduleItem.start_time <= week_end
    ).order_by(ScheduleItem.start_time).all()
    
    # Preparar estructura de días para el mini calendario
    week_days = []
    for i in range(7):
        day = today + timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time())
        day_end = datetime.combine(day, datetime.max.time())
        
        # Contar eventos de ese día
        day_events_count = sum(1 for event in week_events 
                               if day_start <= event.start_time <= day_end)
        
        week_days.append({
            'date': day,
            'day_name': day.strftime('%a')[:3],  # Lun, Mar, etc.
            'day_number': day.day,
            'is_today': (day == today),
            'events_count': day_events_count
        })
    
    return render_template('dashboard.html', tasks=tasks, events=events, 
                         week_days=week_days, today=today)

    if not isLogged():
        return redirect(url_for('auth.login'))
    if session.pop('show_coins_message', False):
        flash("¡Has ganado 10 monedas! 🪙", "coins_success")
    return render_template('dashboard.html')
