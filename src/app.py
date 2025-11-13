from flask import Flask, redirect, url_for
import os
import sys
from database import db
from config import config
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.activitys import activity_bp
from routes.movies import movies_bp
from routes.tasks import tasks_bp
from routes.schedule import schedule_bp
from routes.nutrition import nutrition_bp
from routes.games import games_bp
from routes.study import study_bp
from routes.workout import workout_bp
from utils import inject_user_coins

sys.path.append("../src")

# Obtener el entorno desde variable de entorno, por defecto 'development'
env = os.getenv('FLASK_ENV', 'development')
# Crear la aplicación Flask
app = Flask(__name__)

# Cargar configuración según el entorno
app.config.from_object(config[env])

# Mostrar información de debug sobre la conexión
print(f"DEBUG: Entorno actual: {env}")
print(f"DEBUG: Conectando a la base de datos: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Inicializar la base de datos con la aplicación
db.init_app(app)



app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(activity_bp)
app.register_blueprint(movies_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(schedule_bp)
app.register_blueprint(games_bp)
app.register_blueprint(study_bp)
app.register_blueprint(nutrition_bp)
app.register_blueprint(workout_bp)


app.context_processor(inject_user_coins)

#########


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True,host = '0.0.0.0')